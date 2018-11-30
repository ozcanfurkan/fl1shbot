#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import *
from telegram import * 
import logging,commands,os,random,string,json,urllib,urllib2,re,base64 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO) 
logger = logging.getLogger(__name__) 
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Merhaba!')
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error) 
langlist = ["az","sq","am","en","ar","hy","af","eu","ba","be","bn", 
"my","bg","bs","cy","hu","vi","ht","gl","nl","mrj","el","ka","gu","da", 
"he","yi","id","ga","it","is","es","kk","kn","ca","ky","zh","ko","xh", 
"km","lo","la","lv","lt","lb","mg","ms","ml","mt","mk","mi","mr","mhr", 
"mn","de","ne","no","pa","pap","fa","pl","pt","ro","ru","ceb","sr","si", 
"sk","sl","sw","su","tg","th","tl","ta","tt","te","tr","udm","uz","uk", 
"ur","fi","fr","hi","hr","cs","sv","gd","et","eo","jv","ja"]
kufurlist = [u"amk",u"aq",u"amcık",u"orospu",u"fahişe",u"götveren",u"amını",u"mk", 
u"yavşak",u"piç",u"siktir",u"gavat",u"gevende",u"amına",u"göt",u"mq",u"amı",u"aqü", 
u"yarrak",u"yaraq",u"yarak",u"sikiş",u"porn",u"kaşar",u"şerefsiz",u"orspu",u"arvadını",u"am",u"amkzz",u"amq",u"zzamkzz",u"dingil",u"zzamk",u"amıcık",u"oç",u"osbir",u"yarrağı",u"fetiş",u"fetişim",u"fetişin",u"fetişi",u"siker",u"sikerim",u"sikersin",u"otuzbir", 
u"sikerler",u"sikeni",u"bok",u"sikişme",u"porno",u"sikişmek",u"boklu",u"otuz bir", 
u"sikişmiş",u"pezevenk",u"pezevemk",u"pezeveng",u"pezevemg",u"sg",u"sgmk",u"yarağı",u"sikiyorum",u"sikiyorsun",u"sikiyorlar",u"sikiyom",u"sikiyosun",u"sikiyolar", 
u"fuck",u"bitch",u"pussy",u"bastard",u"ass",u"asshole",u"pussyhole",u"pornstar", 
u"fuk",u"fak",u"sikeyim",u"sikiyim",u"döl",u"dölü",u"amq",u"bisikerim",u"bisikerm", 
u"bisikrm",u"siktiğimin",u"siktimin",u"piçi",u"piçsin",u"piçleri",u"piçler",u"piçim", 
u"amın",u"amınoğlu",u"lavuk",u"oruspu",u"orspu",u"hasiktir",u"hassiktir",u"amınıza",u"gotünüzü",u"orusbu"]
slaplist = [u"{}, {} üzerine tüplü TV fırlattı!", u"{}, {}'ye osmanlı tokadı attı!", u"{}, {} üzerine benzin döktü ve ateşe verdi!", u"{}, {} üzerine iPhone3GS fırlattı!", u"{}, {}'nin RTX 2080Ti'sini kırdı!"] 
transkey = "Yandex-Translate-Token" 
TOKEN = "Telegram-Bot-Token" 
lastrn = -1 
def conv(bot, update):
	res=""
	txt=update.message.text
	if not bool(txt):
		txt=update.message.caption
	global tx
	send=True
	try:
		tx=txt.split(" ")
	except:
		return
	else:
		cmd=tx[0]
		if len(cmd) < 1:
			send=False
			return
		if cmd[0] in ["/","!","\\","|"]:
			txt=txt[len(cmd)+1:]
			if "@" in cmd:
				t = cmd.split("@")
				if bot.username == t[1]:
					cmd=t[0]
				else:
					send=False
					return
			cmd=cmd[1:]
			if "hello" == cmd:
				res = "Merhaba dünya!"
			elif "tekrarla" == cmd:
				if len(txt) > 0:
					res = txt
				else:
					res = "Bu özelliği kullanmak için bir metin yazmalısınız!\nKullanım şekli:\n/tekrarla <metin>"
			elif "id" == cmd:
				type = update.message.chat.type
				res = u"Konuşma tipi: "+type+"\n"+u"Konuşma numarası: "+str(update.message.chat.id)
				if "group" in type:
					res = res + "\n"+u"Kişi numarası: "+str(update.message.from_user.id)
					res = res + "\n"+u"Yöneticiler: "
					for i in bot.get_chat_administrators(update.message.chat.id):
						if bool(i.user.username):
							user = i.user.username
						else:
							user = i.user.full_name
						res = res + "\n" + user + "\n" + i.status + "\n\n"
			elif cmd in [u"duck",u"google",u"stackoverflow",u"wiki"]:
				res = arama(cmd,txt)
			elif cmd in [u"cevir",u"çevir"]:
				if len(txt) > 0:
					if tx[1][1:] in langlist:
						lang = tx[1][1:]
						txt = ''.join(txt).replace(tx[1],"")
					else:
						lang = "tr"
					res = cevir(lang,txt)
				else:
					res = "Bu özelliği kullanmak için bir metin yazmalısınız!\nKullanım şekli:\n/cevir <metin> veya /cevir -dil metin"
			elif "beniat" == cmd:
				if adminctrl(bot,update,update.message.from_user.id):
					user = update.message.from_user.username
					if not bool(user):
						user = update.message.from_user.full_name
					id = update.message.from_user.id
					if adminctrl(bot,update,bot.id):
						try:
							bot.kickChatMember(chat_id=update.message.chat.id,user_id=id)
							bot.unbanChatMember(chat_id=update.message.chat.id,user_id=id)
						except:
							return
						else:
							res = u"@" + user + u" kendisini gruptan attırdı!"
							bot.sendMessage(chat_id=update.message.chat.id,text=res)
							return
					else:
						res = u"Yönetici izinlerine sahip olmadığımdan seni atamıyorum!"
				else:
					res = u"Sen bir yöneticisin, seni engelleyemem!"
			elif "hesapla" == cmd:
				res = os.popen("echo "+txt.replace("(","\(").replace(")","\)").replace(" ","").replace("&","").replace(";","").replace(":","").replace("`","").replace("$","")+" | bc").read()
			elif cmd in [u"tekmele",u"engelle"]:
				try:
					if "group" in update.message.chat.type:
						if adminctrl(bot,update,update.message.from_user.id):
							if len(tx) == 1:
								a = update.message.reply_to_message
								if bool(a):
									if a.from_user.id != bot.id:
										bot.kickChatMember(chat_id=update.message.chat.id,user_id=a.from_user.id)
										if cmd == "engelle":
											res = u"Kişi gruptan atıldı ve engellendi!"
										else:
											bot.unbanChatMember(chat_id=update.message.chat.id,user_id=a.from_user.id)
											res = u"Kişi gruptan atıldı!"
									else:
										res = u"Kendimi nasıl gruptan atabilirim?"
								else:
									res = u"Şu anlık bir kişiyi atmak için o kişinin mesajına cevap vermelisiniz"
							else:
								res = u"Şu anlık bir kişiyi atmak için o kişinin mesajına cevap vermelisiniz"
						else:
							res = u"Yönetici olmadığın için bu yazdığını umursamıyorum"
					else:
						res = u"Bu komut sadece grupta çalışır"
				except:
					res = u"Yönetici izinlerine sahip olmadığımdan veya başka bir sorun oluştuğundan dolayı bu işlemi yapamıyorum"
				else:
					pass
			elif "hava" == cmd:
				res = hava(txt)
			elif "slap" == cmd:
				user = update.message.from_user.username
				us2 = ""
				if not bool(user):
					user = update.message.from_user.full_name
				else:
					user = u"@" + user
				if len(tx) == 1:
					a = update.message.reply_to_message
					if not bool(a):
						us2 = user
						user = u"@"+bot.username
					else:
						b = a.from_user
						if not bool(b.username):
							us2 = b.full_name
						else:
							us2 = "@"+b.username
						send = False
				else:
					us2 = tx[1]
				res = slaplist[rn()].format(user,us2)
				if not send:
					update.message.reply_to_message.reply_text(res)
			else:
				send = False
				#res = "Sizi anlamadım, düzgünce bir daha yazar 
				#mısınız?"
		else:
			#creator = 0 for i in 
			#update.message.chat.get_administrators():
				#if i.status == "creator":
					#creator = i.user.id break
			#if update.message.from_user.id != creator:
			if update.message.chat.id in [-1001479129853]:
				for i in kufurlist:
					if replacer(i) == replacer(txt.lower()) or replacer(i) in replacer(txt.lower()).split(" ") or replacer(i) in replacer(txt.lower()).split("\n"):
						id = update.message.chat.id
						first = update.message.from_user.first_name
						last = update.message.from_user.last_name
						name = first
						if bool(last):
							name = first+" "+last
						uname = update.message.from_user.username
						if not bool(uname):
							uname = str(update.message.from_user.id)
						else:
							uname = "@"+uname
						res = name+u" ("+uname+u")"
						try:
							update.message.delete()
						except:
							if "group" in update.message.chat.type:
								res = res+u" laflarına dikkat et!\nBeni admin yapmayı unutmuşsunuz, mesajları silemiyorum!"
							else:
								res = res+u" laflarına dikkat et!"
						else:
							res = res+u" laflarına dikkat et!"
						bot.sendMessage(chat_id=id,text=res)
						return
					else:
						send = False
			else:
				send = False
			#else:
				#send = False
			# Botla normal sohbet kurma algoritması
			if bot.first_name == tx[0]:
				if len(tx) == 1:
					res = u"Efendim?"
				else:
					if u"nasılsın" in tx[1].lower() or u"naber" in tx[1].lower():
						res = u"Ben bir botum, duygularım yoktur."
					elif u"ne yapıyorsun" in txt[len(tx[0])+1:].lower():
						res = u"Çalışıyorum, sen ne yapıyorsun?"
					else:
						send = False
				send = True
		if send:
				if cmd not in [u"hava",u"duck",u"google",u"stackoverflow",u"wiki"]:
					update.message.reply_text(res)
				else:
					update.message.reply_markdown(res)
				
def replacer(text):
	rep = {u"ç": u"c", u"ğ": u"g", u"ı": u"i", u"ö": u"o",u"ş": u"s", u"ü": u"u"}
	rep = dict((re.escape(k), v) for k, v in rep.iteritems())
	pattern = re.compile("|".join(rep.keys()))
	text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
	return text

tx = []
def inline(bot, update):
	query = update.inline_query.query
	if len(query) > 2:
		global tx
		tx = query.split(" ")
		sres = []
		if tx[0][0] in ["/","!","\\","|"]:
			temp=query[len(tx[0])+1:]
			cmd=tx[0][1:]
			desc = ""
			if "tekrarla" == cmd:
				desc="Metni tekrarla: "+temp
				if len(tx) < 2:
					desc="Bu özelliği kullanmak için bir metin yazmalısınız!\nKullanım şekli:\n/tekrarla <metin>"
					temp=desc
				sres.append(InlineQueryResultArticle(
						id = ''.join(random.choice(string.ascii_lowercase + string.digits))[:8],
						title = bot.first_name,
						#thumb_url = "http://python-telegram-bot.readthedocs.io/en/latest/_static/ptb-logo-orange.png",
						description=desc,
						input_message_content = InputTextMessageContent(temp)
					)
				)
			
			elif cmd in [u"duck",u"google",u"stackoverflow",u"wiki"]:
				desc = u"🔍 " + arasite(cmd) + ": " + temp
				temp = arama(cmd,temp)
				sres.append(InlineQueryResultArticle(
						id = ''.join(random.choice(string.ascii_lowercase + string.digits))[:8],
						title = bot.first_name,
						#thumb_url = "http://python-telegram-bot.readthedocs.io/en/latest/_static/ptb-logo-orange.png",
						description=desc,
						input_message_content = InputTextMessageContent(temp,parse_mode=ParseMode.MARKDOWN)
					)
				)
			elif "hava" == cmd:
				if len(tx) < 2:
					desc="Bu özelliği kullanmak için bir metin yazmalısınız!\nKullanım şekli:\n/hava <şehir>"
					temp=desc
				else:
					desc = u"Hava durumu: "+temp
					temp = hava(temp)
				sres.append(InlineQueryResultArticle(
						id = ''.join(random.choice(string.ascii_lowercase + string.digits))[:8],
						title = bot.first_name,
						#thumb_url = "http://python-telegram-bot.readthedocs.io/en/latest/_static/ptb-logo-orange.png",
						description=desc,
						input_message_content = InputTextMessageContent(temp,parse_mode=ParseMode.MARKDOWN)
					)
				)
			elif cmd in [u"cevir",u"çevir"]:
				desc=u"Çevir: "+temp
				if len(tx) < 2:
					desc="Bu özelliği kullanmak için bir metin yazmalısınız!\nKullanım şekli:\n/cevir <metin> veya /cevir -dil metin"
					temp=desc
				else:
					if tx[1][1:] in langlist:
						lang = tx[1][1:]
						temp = ''.join(temp).replace(tx[1],"")
						desc = ''.join(desc).replace(tx[1],"") + " -> " + lang
					else:
						lang = "tr"
					#print(lang)
					temp = cevir(lang,temp)
					desc = desc + "\n" + u"Önizleme: " + temp
				sres.append(InlineQueryResultArticle(
						id = ''.join(random.choice(string.ascii_lowercase + string.digits))[:8],
						title = bot.first_name,
						#thumb_url = "http://python-telegram-bot.readthedocs.io/en/latest/_static/ptb-logo-orange.png",
						description=desc,
						input_message_content = InputTextMessageContent(temp)
					)
				)
			else:
				return
			update.inline_query.answer(sres)
		else:
			return
	else:
		return 

def welcome(bot, update):
	update.message.reply_text("Merhaba, gruba hoş geldin. Kendini tanıtır mısın?")
	
def goodbye(bot, update):
	update.message.reply_text("Hoşçakal 🖐")
	
def adminctrl(bot,update,id):
	for i in bot.get_chat_administrators(update.message.chat.id):
		if id == i.user.id:
			return True
	return False 

def rn():
	global lastrn
	xrn = random.randint(0,len(slaplist)-1)
	if xrn != lastrn:
		lastrn = xrn
		return lastrn
	return rn()

def hava(sehir):
	if not bool(sehir):
		return u"Lütfen bir şehir adı girin"
	sehir = sehir.replace(sehir[0],sehir[0].upper(),1)
	txt = urllib.quote(sehir.encode("utf8"))
	txt = urllib2.Request("http://wttr.in/"+txt+"?qT0", headers={'User-agent': 'curl/7.23', 'Accept-language': 'tr'})
	txt = urllib2.urlopen(txt).read()
	if not bool(txt):
		return u"Bu özellik şu anda çalışmıyor"
	txtx = txt.replace(txt.split("\n")[0],"",1)
	txtx = "```%s```" % txtx
	#.replace("Turkey","Türkiye")
	txtx = txt.split("\n")[0] + "\n" + txtx
	return txtx

def cevir(dil,cumle):
	temp = urllib.quote(cumle.encode("utf8"))
	temp = ''.join(temp).replace("?","%3F")
	temp = "https://translate.yandex.net/api/v1.5/tr.json/translate?key="+transkey+"&lang="+dil+"&text="+temp
	#print temp
	temp = urllib2.urlopen(temp)
	temp = json.loads(temp.read()).get("text")[0]
	return temp
	
def arama(cmd,cumle):
	res = cumle
	txt = cumle
	if res in tx[0]:
		res = u"Lütfen aramak için bir metin yazın"
	else:
		res = urllib.quote(res.encode("utf8"))
		if cmd == "duck":
			res = "https://duckduckgo.com/?q="+res
		elif cmd == "stackoverflow":
			res = "https://stackoverflow.com/search?q="+res
		elif cmd == "wiki":
			res = base64.b64encode("https://tr.wikipedia.org/w/index.php?search="+res)
			res = "http://www.wikizeroo.net/index.php?q="+res
		else:
			res ="https://www.google.com.tr/search?q="+res
		txt = "[%s]" % txt
		res = "(%s)" % res
		res = u"🔍 " + ("*%s*" % arasite(cmd) + ": ") + txt + res
		return res

def arasite(cmd):
	if cmd == "duck":
		return "DuckDuckGo"
	elif cmd == "stackoverflow":
		return "Stack Overflow"
	elif cmd == "wiki":
		return "Wikizero"
	else:
		return "Google"
		
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, 
welcome))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, 
goodbye))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(InlineQueryHandler(inline))
    dp.add_handler(MessageHandler(Filters.all, conv))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
