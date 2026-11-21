# AfinoAi — Android / Pydroid 3
# Python 3.13 • Kivy 2.3.1 • OpenRouter
import os, json, threading
import requests
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

API="https://openrouter.ai/api/v1"
BG=(0.055,0.055,0.085,1)
PANEL=(0.10,0.09,0.15,1)
PURPLE=(0.48,0.30,0.95,1)
TEXT=(0.94,0.93,0.98,1)
MUTED=(0.65,0.64,0.72,1)

class AfinoAI(App):
    def build(self):
        self.title="AfinoAi"
        Window.clearcolor=BG
        self.data_path=os.path.join(self.user_data_dir,"afino_data.json")
        self.data=self.load_data()
        self.api_key=self.data.get("api_key","")
        self.model=self.data.get("model","openrouter/free")
        self.messages=self.data.get("messages",[])
        self.search_mode=False
        self.reason_mode=False
        root=BoxLayout(orientation="vertical",padding=dp(12),spacing=dp(9))
        header=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(8))
        header.add_widget(Label(text="[b]Afino[/b][color=9A70FF]Ai[/color]",markup=True,
                                font_size="24sp",halign="left"))
        header.add_widget(self.btn("Модель",self.model_popup,width=dp(90)))
        header.add_widget(self.btn("Настройки",self.settings,width=dp(100)))
        root.add_widget(header)
        self.status=Label(text="Ваш интеллектуальный помощник",size_hint_y=None,height=dp(25),
                          color=MUTED,font_size="12sp")
        root.add_widget(self.status)
        self.chat=GridLayout(cols=1,spacing=dp(9),size_hint_y=None,padding=[0,dp(5)])
        self.chat.bind(minimum_height=self.chat.setter("height"))
        scroll=ScrollView(do_scroll_x=False)
        scroll.add_widget(self.chat)
        root.add_widget(scroll)
        modes=BoxLayout(size_hint_y=None,height=dp(42),spacing=dp(8))
        self.search_btn=self.btn("⌕ Поиск: выкл.",self.toggle_search)
        self.reason_btn=self.btn("◈ Рассуждение: выкл.",self.toggle_reason)
        modes.add_widget(self.search_btn); modes.add_widget(self.reason_btn)
        root.add_widget(modes)
        composer=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(7))
        self.input=TextInput(hint_text="Напишите сообщение…",multiline=False,
                             background_color=PANEL,foreground_color=TEXT,
                             hint_text_color=MUTED,cursor_color=PURPLE,
                             padding=[dp(12),dp(14)])
        self.input.bind(on_text_validate=lambda *_:self.send())
        composer.add_widget(self.input)
        composer.add_widget(self.btn("➤",self.send,width=dp(52)))
        root.add_widget(composer)
        self.token_label=Label(text="Afino Tokens · локальный демо-баланс",size_hint_y=None,
                               height=dp(24),color=MUTED,font_size="11sp")
        root.add_widget(self.token_label)
        self.refresh_chat()
        return root

    def btn(self,text,callback,width=None):
        b=Button(text=text,size_hint_x=None if width else 1,width=width,
                 background_normal="",background_color=PURPLE,color=TEXT,
                 font_size="13sp")
        b.bind(on_release=lambda *_:callback())
        return b

    def load_data(self):
        try:
            with open(self.data_path,"r",encoding="utf-8") as f:return json.load(f)
        except: return {}

    def save(self):
        self.data.update({"api_key":self.api_key,"model":self.model,"messages":self.messages})
        try:
            with open(self.data_path,"w",encoding="utf-8") as f:json.dump(self.data,f,ensure_ascii=False)
        except: pass

    def refresh_chat(self):
        self.chat.clear_widgets()
        if not self.messages:
            self.add_bubble("AfinoAi","Привет! Я AfinoAi. Введите API-ключ в настройках OpenRouter и задайте вопрос.")
        else:
            for m in self.messages[-60:]:
                self.add_bubble("Вы" if m["role"]=="user" else "AfinoAi",m["content"])

    def add_bubble(self,who,text):
        outer=BoxLayout(orientation="vertical",size_hint_y=None,padding=dp(11),spacing=dp(4))
        outer.bind(minimum_height=outer.setter("height"))
        title=Label(text=who,size_hint_y=None,height=dp(20),color=PURPLE if who=="AfinoAi" else MUTED,
                    halign="left",font_size="12sp")
        title.bind(size=lambda w,s:setattr(w,"text_size",s))
        body=Label(text=text,size_hint_y=None,color=TEXT,halign="left",valign="top",
                   font_size="14sp")
        body.bind(width=lambda w,v:setattr(w,"text_size",(v, None)))
        body.bind(texture_size=lambda w,v:setattr(w,"height",v[1]+dp(8)))
        outer.add_widget(title); outer.add_widget(body)
        outer.height=dp(40)+body.height
        outer.canvas.before # keep layout simple; no custom canvas drawing
        self.chat.add_widget(outer)

    def toggle_search(self):
        self.search_mode=not self.search_mode
        self.search_btn.text="⌕ Поиск: "+("вкл." if self.search_mode else "выкл.")

    def toggle_reason(self):
        self.reason_mode=not self.reason_mode
        self.reason_btn.text="◈ Рассуждение: "+("вкл." if self.reason_mode else "выкл.")

    def settings(self):
        box=BoxLayout(orientation="vertical",padding=dp(12),spacing=dp(10))
        key=TextInput(text=self.api_key,hint_text="OpenRouter API key",password=True,multiline=False,
                      size_hint_y=None,height=dp(48))
        box.add_widget(Label(text="Ключ хранится локально на устройстве.",color=MUTED))
        box.add_widget(key)
        save=self.btn("Сохранить",lambda:None)
        pop=Popup(title="Настройки AfinoAi",content=box,size_hint=(.92,.42))
        def store(*_):
            self.api_key=key.text.strip(); self.save(); pop.dismiss()
            self.status.text="Настройки сохранены"
        save.bind(on_release=store); box.add_widget(save); pop.open()

    def model_popup(self):
        box=BoxLayout(orientation="vertical",padding=dp(10),spacing=dp(8))
        box.add_widget(Label(text="Текущая модель: "+self.model,color=TEXT))
        choices=["openrouter/free"]
        try:
            r=requests.get(API+"/models",timeout=15)
            if r.ok:
                for item in r.json().get("data",[]):
                    p=item.get("pricing",{})
                    if str(p.get("prompt"))=="0" and str(p.get("completion"))=="0":
                        choices.append(item["id"])
        except: pass
        for name in choices[:30]:
            box.add_widget(self.btn(name,lambda n=name:self.choose_model(n)))
        pop=Popup(title="Выбор модели",content=ScrollView(size_hint=(1,1)),size_hint=(.9,.8))
        pop.content.add_widget(box); self._model_pop=pop; pop.open()

    def choose_model(self,name):
        self.model=name; self.save()
        if hasattr(self,"_model_pop"):self._model_pop.dismiss()
        self.status.text="Модель: "+name

    def send(self):
        prompt=self.input.text.strip()
        if not prompt:return
        if not self.api_key:
            self.status.text="Сначала добавьте API-ключ в настройках"
            self.settings(); return
        self.input.text=""
        self.messages.append({"role":"user","content":prompt})
        self.add_bubble("Вы",prompt); self.status.text="AfinoAi думает…"
        self.save()
        threading.Thread(target=self.request_ai,args=(prompt,),daemon=True).start()

    def request_ai(self,prompt):
        system="Ты AfinoAi — полезный русскоязычный AI-помощник. Отвечай ясно и по делу."
        if self.reason_mode: system+=" Внимательно анализируй задачу и проверяй выводы перед ответом."
        if self.search_mode: system+=" Если доступен инструмент поиска, используй актуальные источники; не выдумывай результаты веб-поиска."
        payload={"model":self.model,"messages":[{"role":"system","content":system}]+self.messages[-30:],
                 "stream":False,"max_tokens":1800}
        try:
            r=requests.post(API+"/chat/completions",headers={
                "Authorization":"Bearer "+self.api_key,"Content-Type":"application/json",
                "HTTP-Referer":"https://github.com/slow22852-star/AfinoAi","X-Title":"AfinoAi"
            },json=payload,timeout=90)
            if r.status_code>=400:
                try: err=r.json().get("error",{}).get("message",r.text)
                except: err=r.text
                answer="Ошибка API: "+str(err)
            else: answer=r.json()["choices"][0]["message"]["content"]
        except Exception as e: answer="Не удалось подключиться: "+str(e)
        Clock.schedule_once(lambda dt:self.finish(answer),0)

    def finish(self,answer):
        self.messages.append({"role":"assistant","content":answer})
        self.add_bubble("AfinoAi",answer); self.status.text="Готово"; self.save()

if __name__=="__main__":
    AfinoAI().run()
