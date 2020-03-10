# coding: utf-8

import requests
import re
import subprocess
import glob
import sys
import os
import asyncio
import aiohttp
from aiohttp import FormData
import json
import requests
#from random import randint
#ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

oriIndexM3u8 = ''
async def doupdateByAli(session, filePath):
	global oriIndexM3u8	
	ffpp = os.path.join(filePath.replace('/','\\'))
	filePath = ffpp
	fname= filePath.split('\\')[-1]
	ftype = fname.split('.')[1]
	if ftype not in ['jpg','png','gif','jpeg']:
		fname = fname + '%20.jpg'
	url="https://kfupload.alibaba.com/mupload"
	#files ={'file':(fname,open(filePath,'rb').read(),'application/octet-stream')}
	headers = {'Accept':'application/json','Accept-Encoding':'gzip,deflate,sdch','User-Agent':'iAliexpress/6.22.1 (iPhone; iOS 12.1.2; Scale/2.00)'}

	datas={'name':fname,'scene':'aeMessageCenterV2ImageRule'}
	data = FormData()
	data.add_field('file',
               open(filePath, 'rb'),
               filename=fname,
               content_type='application/octet-stream',
               )
	data.add_field(name='name',value=fname)
	data.add_field(name='scene',value='aeMessageCenterV2ImageRule')
 
	flag = True
	errTimes = 0
	while flag:
		try:
			resp = await session.post(url,data=data,headers=headers)
			resp.ecoding = 'utf-8'
			url = await resp.text()
			#url='{"fs_url":"Hd41b648b25eb43c6a4cec4cbb2bc7e15U.jpg","code":"0","size":"896196","width":"0","url":"https://ae01.alicdn.com/kf/Hd41b648b25eb43c6a4cec4cbb2bc7e15U.jpg","hash":"1d1ef4b1d194031a2a9e54f3ec157ad4","height":"0"}'
			#print(url)
			if url:
				flag = False
				#os.remove(filePath)
				newV = json.loads(url)['url']
				print(fname,'->',newV)
				return newV
		except Exception as e:
			errTimes=errTimes+1
			if errTimes>10:
				flag=False
			print('get error',e)
	#resp.coding='utf-8'
	#return resp.json()['url']


async def main(loop,arg1,arg2):
	global oriIndexM3u8
	async with aiohttp.ClientSession() as session:
		all_file_list = []
		if arg1 == '-p':
			all_file_list = glob.glob(arg2+'/*.*')
		elif arg1 == '-f':
			all_file_list.append(arg2)
		print(all_file_list)
		tasks=[]
		for _ in all_file_list:
			print(_)
			tasks.append(loop.create_task(doupdateByAli(session,_)))

		finished , unfinished = await asyncio.wait(tasks)

#doupdateByAli("C:/Users/Admin/Desktop/M3U8Download/mp4/1.jpg")
#vToTs('./tet','C:/Users/Admin/Desktop/M3U8Download/output/FYQM01.mp4')
arg1_fileORpath = sys.argv[1]
arg2_pv = sys.argv[2]

print(arg1_fileORpath,arg2_pv)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop,arg1_fileORpath,arg2_pv))
loop.close()
