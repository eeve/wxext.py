# -*- coding: utf-8 -*-

import os
import requests, re, time, random, sys, hashlib
import xml.etree.ElementTree as ET
from pyquery import PyQuery as pq
import configparser
import codecs

cp = configparser.SafeConfigParser()
with codecs.open('app.conf', 'r', encoding='utf-8') as f:
    cp.readfp(f)


print()


gmsg = ['']

headers = {
	'Host': 'bbs.pcbeta.com',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
	'Origin': 'http://bbs.pcbeta.com',
	'Referer': 'http://bbs.pcbeta.com',
	'Accept-Encoding': 'identity'
}

session = requests.Session()
session.headers.update(headers)


'''
添加日志
'''
def appendLog(log):
	gmsg.append(log)

'''
md5
'''
def md5(password):
	pwd = hashlib.md5()
	pwd.update(str(password).encode('utf-8'))
	return pwd.hexdigest()


'''
登录
'''
def login():
	loginUrl = 'http://bbs.pcbeta.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LIXeh&inajax=1'
	payload = {
		'formhash': 'd68fd158',
		'referer': 'http://bbs.pcbeta.com/',
		'username':	cp.get('pcbeta', 'account'),
		'password': cp.get('pcbeta', 'password'),
		'questionid': '0',
		'answer': ''
	}
	r = session.post(loginUrl, data=payload)
	text = r.text
	# print(requests.utils.dict_from_cookiejar(r.cookies))
	root = ET.fromstring(text)
	if '现在将转入登录前页面' in root.text:
		appendLog('登录成功！')
	else:
		appendLog('登录失败: %s' % root.text)


'''
回复
'''
def pre_reply(url=None, message='顶上去让大家看到！！！'):
	html = session.get(url).text
	# 匹配出formhash
	m = re.search(r'name="formhash" value="([A-Za-z0-9]{8})"', html)
	if m is None:
		raise RuntimeError('未能匹配到帖子的回帖formhash！')
	formhash = m.group(1)
	appendLog('匹配到的formhash为：%s' % formhash)

	# 匹配出fid
	m = re.search(r'fid = parseInt\(\'(\d+)\'\)', html)
	if m is None:
		raise RuntimeError('未能匹配到帖子的fid！')
	fid = m.group(1)
	appendLog('匹配到的fid为：%s' % fid)

	# 匹配出tid
	m = re.search(r'tid = parseInt\(\'(\d+)\'\);', html)
	if m is None:
		raise RuntimeError('未能匹配到帖子的tid！')
	tid = m.group(1)
	appendLog('匹配到的tid为：%s' % tid)

	# 匹配出idhash
	m = re.search(r'<input\sname="sechash"\stype="hidden"\svalue="([A-Za-z0-9]{8})"\s/>', html)
	if m is None:
		idhash = None
	else:
		idhash = m.group(1)
	appendLog('匹配到的idhash为：%s' % idhash)

	fileName = None
	validRealUrl = None
	if idhash is not None:
		appendLog('签到需要填写验证码！')
		# 获取新验证码图片的URL
		validImageUrl = 'http://bbs.pcbeta.com/misc.php?mod=seccode&action=update&idhash=%s&inajax=1&ajaxtarget=seccode_%s' % (idhash, idhash)
		root = ET.fromstring(session.get(validImageUrl).text)
		m = re.match(r'.*src="(misc\.php\?mod=seccode&update=\d+&idhash=[A-Za-z0-9]+)".*', root.text)
		if m is None:
			raise RuntimeError('未能获取到新验证码的URL')
		validRealUrl = 'http://bbs.pcbeta.com/' + m.group(1)
		appendLog('新验证码的url: %s' % validRealUrl)

		# 获取新的验证码并保存
		fileName = 'valid.png'
		ir = session.get(validRealUrl)
		if ir.status_code == 200:
			open(fileName, 'wb').write(ir.content)

	return {
		'message': message,
		'formhash': formhash,
		'fid': fid,
		'tid': tid,
		'idhash': idhash,
		'validRealUrl': validRealUrl,
		'validFileName': fileName
	}


def after_reply(tiezi):

	if(tiezi['idhash'] is not None and tiezi['validRealUrl'] is not None):
		# 需要校验码
		appendLog('校验码为：%s' % tiezi['validCode'])
		# 提交验证码，进行验证
		submitValidImageUrl = 'http://bbs.pcbeta.com/misc.php?mod=seccode&action=check&inajax=1&&idhash=%s&secverify=%s' % (tiezi['idhash'], tiezi['validCode'])
		root = ET.fromstring(session.get(submitValidImageUrl).text)
		if 'succeed' not in root.text:
			raise RuntimeError('验证码校验失败，验证码错误！')
		else:
			appendLog('本次回复不需要验证码！')

	# 提交回复
	replyUrl = 'http://bbs.pcbeta.com/forum.php?mod=post&action=reply&fid=%s&tid=%s&extra=page%%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1' % (tiezi['fid'], tiezi['tid'])

	data = {
		'message': tiezi['message'].encode('gb2312'),
		'posttime': int(time.time()),
		'formhash': tiezi['formhash'],
		'usesig': '1',
		'subject': ''
	}

	if tiezi['idhash'] is not None:
		data.sechash = tiezi['idhash']
		data.seccodeverify = tiezi['validCode']
	else:
		delay = random.randint(3, 6)
		appendLog('等待%ss...' % delay)
		time.sleep(delay)

	root = ET.fromstring(session.post(replyUrl, data=data).text)
	if '回复需要审核，请等待通过' in root.text:
		appendLog('回复成功，但需要审核！')
	elif '非常感谢，回复发布成功' in root.text:
		appendLog('回复成功！')
	else:
		appendLog('回复失败：%s' % root.text)

'''
获取做任务的帖子URL
'''
def getTaskUrl():
	url = 'http://bbs.pcbeta.com/forum.php?mod=forumdisplay&fid=16&filter=typeid&typeid=1217'
	d = pq(session.get(url).text)
	postUrl = d('#separatorline').next().find('.new').find('a').eq(1).attr('href')
	appendLog('最新的任务帖子url: %s' % postUrl)
	return postUrl


'''
每日签到任务
'''
def task():
	# 申请
	url = 'http://i.pcbeta.com/home.php?mod=task&do=apply&id=119'
	html = session.get(url).text
	d = pq(html)
	status = d('#messagetext').find('p').text()
	if '任务申请成功' in status:
		appendLog('任务申请成功')
	elif '本期您已申请过此任务' in status:
		appendLog('今天已经申请了此任务')
	else:
		appendLog('任务申请失败！%s' % status)


'''
领奖
'''
def done():
	url = 'http://i.pcbeta.com/home.php?mod=task&do=draw&id=119'
	html = session.get(url).text
	d = pq(html)
	status = d('#messagetext').find('p').text()
	if '您还没有开始执行任务' in status:
		appendLog('请先执行任务！')
		return False
	elif '恭喜您，任务已成功完成' in status:
		appendLog('恭喜，任务完成！')
		return True
	else:
		appendLog(status)
		return False


'''
回复内容列表
'''
contents = [
	'看帖回帖好习惯，谢谢分享。',
	'每日围观签到',
	'远景因你们而精彩',
	'每天签到，支持远景',
	'每日一签好习惯！',
	'看帖回帖好习惯',
	'每天都来领个福利',
	'看看每日景讯 %s' % time.strftime("%Y-%m-%d %H:%M"),
	'签到，领取奖励，希望远景越来越好',
	'支持远景！前来报到！',
	'感谢远景一路陪伴',
	'感谢远景的一路陪伴{:5_262:}',
	'{:5_264:}各位大家好',
	'来一波，强行签到，强行签到！',
	'每天签到支持远景论坛{:5_293:}'
]

'''
签到
'''
def qiandao():
	login()
	task() # 领任务
	text = contents[random.randint(0, len(contents) - 1)]
	appendLog('将要回复的内容: %s' % text)

	tiezi = pre_reply(url=getTaskUrl(), message=text) # 做任务
	after_reply(tiezi)

	if done(): # 领奖
		return '签到成功！\n  ----- log details ----- \n %s' % '\r'.join(gmsg)
	else:
		return '签到失败！\n  ----- log details----- \n %s' % '\r'.join(gmsg)


def doAction(tieziUrl, content):
	if tieziUrl is None:
		qiandao()
	else:
		print('>> 指定帖子url: %s' % tieziUrl)
		if content is not None:
			message = content
		else:
			message = contents[random.randint(0, len(contents) - 1)]
		print('>> 指定回复帖子内容: %s' % message)
		login()
		tiezi = pre_reply(tieziUrl, message)
		after_reply(tiezi)

# python3 pcbeta.py http://xxxx 恭喜楼主！
if __name__ == '__main__':
	param = sys.argv
	if(len(param) < 3):
		print('至少需要两个参数:[帖子url, 回复content]')
	else:
		msg = doAction(param[1], param[2])
		print(msg)
		print('%s' % '\r'.join(gmsg))
