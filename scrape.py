from pyrogram import Client
import base64
import re
import json
import os


isValid = True
cfgFileFormat = [
    'ehi',
    'hc',
    'inpv',
    'npv4',
    'dark',
    'alph'
]
vpnNames = [
    'vpn',
    'tunnel',
    'tunel',
    'فیلترشکن',
    'فیلتر شکن',
    'وی پی ان',
    'فیلتر'
]


#PRESET STUFF, CHANGE WITH YOUR PRESETS!
cId = "target chat id"
msgPreset = f'''add a preset for the messages'''
cfgName = 'add a name for configs, bot will change vless vmess config names and file names to this'
#private shit
app = Client(
    "my_account",
    api_id=,
    api_hash=''
)

@app.on_message()
async def my_handler(client, message):

    if message.text and len(message.text) > 40:

        #find vless and trojan and ss
        notb64Msg = re.findall(r'vless:\/\/\S+|trojan:\/\/\S+|\bss:\/\/\S+', message.text)
        if len(notb64Msg) > 0:
            for item in notb64Msg:
                cfgToSend = notb64(item)
                await app.send_message(cId, f'`{cfgToSend}`{msgPreset}')

        #find vmess
        vmess = re.findall(r'vmess:\/\/\S+', message.text)
        if len(vmess) > 0:
            for item in vmess:
                cfgToSend = vmessFunc(item)
                await app.send_message(cId, f'`{cfgToSend}`{msgPreset}')

        #find darktun
        darkTun = re.findall(r'darktunnel:\/\/\S+', message.text)
        if len(darkTun) > 0:
            for item in darkTun:
                cfgToSend = darkTunFunc(item)
                await app.send_message(cId, f'`{cfgToSend}`{msgPreset}')

        #find matsuri links
        matsuri = re.findall(r'sn:\/\/\w+\?\S+', message.text)
        for item in matsuri:
            await app.send_message(cId, f'`{item}`{msgPreset}')

        #find telegram proxies
        proxyMsg = re.findall(r'https:\/\/t\.me\/\w+\?server=\S+', message.text)
        if len(proxyMsg) > 0:
            
            #no need to make another func. since proxies dont have a name to change, we just send them no problemo!
            for item in proxyMsg:
                cfgToSend = item
                await app.send_message(cId, f'{cfgToSend}{msgPreset}')

    #find .ehi .inpv .inv4.... and apk files
    if message.document:
        fileFormat = message.document.file_name.split('.')[-1]
        fileName = message.document.file_name.split('.')[0].lower()
        
        if fileFormat == 'apk':
            if any(ele in fileName for ele in vpnNames):
                await message.copy(chat_id=cId, caption=msgPreset)
         
        if fileFormat in cfgFileFormat:
            await app.download_media(message.document.file_id, file_name=f'{cId}.{fileFormat}')
            await app.send_document(chat_id=cId ,document=f'downloads/{cId}.{fileFormat}', caption=msgPreset)
            os.remove(f'downloads/{cId}.{fileFormat}')


#change name for vless and trojan and ss
def notb64(item):

    #simple af validation!
        
    #is name already set?
    if '#' in item:
        tempItem = item.split('#')
        tempItem = f'{tempItem[0]}#{cfgName}'
        cfg = ''.join(f'{tempItem}\n')
        return cfg
        
    #name is not already set. just add it
    else:
        cfg = f'{item}#{cfgName}\n'
        return cfg


#change name for vmess
def vmessFunc(item):
    tempItem = item.replace('vmess://', '')
    decoded = base64.b64decode(tempItem).decode('utf-8')
    tempDict = json.loads(decoded)
    tempDict['ps'] = cfgName
    encoded = base64.b64encode(json.dumps(tempDict).encode('utf-8')).decode('ascii')
    cfg = f'vmess://{encoded}\n'
    return cfg


def darkTunFunc(item):
    tempItem = item.replace('darktunnel://', '')
    decoded = base64.urlsafe_b64decode(tempItem).decode('utf-8')
    tempDict = json.loads(decoded)
    tempDict['name'] = cfgName
    encoded = base64.b64encode(json.dumps(tempDict).encode('utf-8')).decode('ascii')
    cfg = f'darktunnel://{encoded}\n'
    return cfg


app.run()
