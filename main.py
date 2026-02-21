import flet as ft
import os

DB_FILE = "chat_history.txt"

def main(page: ft.Page):
    page.title = "أصيل ميسنجر"
    page.rtl = True
    chat_list = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    
    def on_broadcast(data):
        if "text" in data:
            chat_list.controls.append(ft.Text(f"{data['user']}: {data['text']}"))
            page.update()

    page.pubsub.subscribe(on_broadcast)
    msg_input = ft.TextField(hint_text="اكتب هنا...", expand=True)

    def send_click(e):
        page.pubsub.send_all({"user": page.session.get("u"), "text": msg_input.value})
        msg_input.value = ""
        page.update()

    page.session.set("u", "مستخدم")
    page.add(ft.Column([chat_list, ft.Row([msg_input, ft.ElevatedButton("إرسال", on_click=send_click)])], expand=True))

if __name__ == "__main__":
    # لاحظ هنا: جعلنا الـ view يساوي None لتجنب أخطاء التحميل
    ft.app(target=main, view=None, port=8502, host="0.0.0.0")
