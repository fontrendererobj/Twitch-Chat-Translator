from socket import socket
import re, os

try:
    import yaml
    from easygoogletranslate import EasyGoogleTranslate
    import pyttsx3
    from colorama import Fore
except ModuleNotFoundError:
    print("You are missing some Modules.. let me fix that.")
    os.system("pip install PyYAML easygoogletranslate pyttsx3 colorama")
    print("Finished installing Modules. Rerun the program.")
    
# Needed for the Colors in Terminal (for windows atleast)
os.system("color")

# Setup Translate
googleTranslate = EasyGoogleTranslate()

# Setup TTS
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[1].id)

# Load Config Values
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)
    
    server = config['server']
    port = config['port']
    nickname = config['nickname']
    token = config['oauth']
    channels = config['channels']
    language = config['language']
    tts = config['tts']
    bot_check = config['bot_check']
    bot_users = config['bot_users']


sock = socket()
sock.connect((server, port))

# Provide Nickname and Oauth to Twitch so we can read the messages.
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))

# Join all Channels from the config
for channel in channels:
    sock.send(f"JOIN #{channel}\n".encode('utf-8'))

while True:
        resp = sock.recv(2048).decode('utf-8')

        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
        
        elif len(resp) > 0:
            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))
                
            elif len(resp) > 0 and 'PRIVMSG' in resp:
                    match = re.search(r':([^!]+)![^@]+@[^ ]+\.tmi\.twitch\.tv PRIVMSG #([^ ]+) :(.+)', resp)
                    if match:
                        username, channel, message = match.groups()
                        
                        # Check if Message is not an Command
                        if not message.startswith("!"):
                            translated_message = googleTranslate.translate(text=message, target_language=language)

                        # TODO make this configurable
                        print(f"{Fore.CYAN} {channel} {Fore.RED} {username}{Fore.LIGHTBLUE_EX}: {Fore.WHITE}{translated_message} | {message}")
                        
                        # Check if TTS is enabled and user is not a Bot.
                        if tts:
                            
                            # ass code but i couldnt care less
                            
                            if bot_check:
                                if not username in bot_users:
                                    engine.say(f"{channel}: {translated_message}")
                                    engine.runAndWait()
                            else:
                                engine.say(f"{channel}: {translated_message}")
                                engine.runAndWait()