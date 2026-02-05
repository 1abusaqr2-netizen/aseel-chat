import flet as ft
import random
import os

# الإعدادات الأمنية
DB_FILE = "chat_history.txt"
ADMIN_PASSWORD = "123" # غير كلمة السر هنا لأي رقم تريده
active_users = {}

def main(page: ft.Page):
    page.title = "أصيل ميسنجر - نظام المدير الآمن"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f4f4f9"
    page.padding = 0

    chat_list = ft.ListView(expand=True, spacing=10, auto_scroll=True, padding=20)
    users_column = ft.Column(spacing=10)

    # دالة مسح الشات (التي سيطلب التطبيق كلمة سر لتنفيذها)
def clear_chat_secure(e):
        pw_input = ft.TextField(label="كلمة سر المدير", password=True, can_reveal_password=True)
        
def confirm_clear(ev):
            if pw_input.value == ADMIN_PASSWORD:
                if os.path.exists(DB_FILE):
                    os.remove(DB_FILE)
                page.pubsub.send_all({"action": "clear"})
dialog.open = False
                page.show_snack_bar(ft.SnackBar(ft.Text("تم تنظيف السيرفر بنجاح")))
                page.update()
            else:
                pw_input.error_text = "كلمة السر خاطئة!"
                page.update()

dialog = ft.AlertDialog(
            title=ft.Text("تأكيد مسح البيانات"),
            content=pw_input,
            actions=[ft.TextButton("إلغاء", on_click=lambda _: setattr(dialog, "open", False) or page.update()),
                     ft.ElevatedButton("مسح الكل", on_click=confirm_clear, bgcolor="red", color="white")]
        )
        page.overlay.append(dialog)
dialog.open = True
        page.update()

def add_message_to_ui(user, text, phone, is_image=False):
        is_me = phone == page.session.get("phone")
        content = ft.Column([ft.Text(user, size=10, color="blue", weight="bold")], spacing=2)
        if is_image:
            content.controls.append(ft.Image(src=text, width=200, border_radius=10))
        else:
            content.controls.append(ft.Text(text, size=16, color="black"))

        chat_list.controls.append(
            ft.Row([
                ft.Container(
                    content=content,
                    bgcolor="#DCF8C6" if is_me else "white",
                    padding=12, border_radius=15, shadow=ft.BoxShadow(blur_radius=1, color="black12")
                )
            ], alignment=ft.MainAxisAlignment.END if is_me else ft.MainAxisAlignment.START)
        )
        page.update()

def update_users_list():
        users_column.controls.clear()
        users_column.controls.append(ft.Text("المتصلون الآن:", weight="bold", color="gold"))
        for phone, name in active_users.items():
            users_column.controls.append(ft.Row([ft.Icon(ft.icons.CIRCLE, color="green", size=10), ft.Text(name, size=14)]))
        page.update()

def on_broadcast(data):
        if data.get("action") == "login":
            active_users[data["phone"]] = data["user"]
            update_users_list()
            return
        if data.get("action") == "clear":
            chat_list.controls.clear()
            page.update()
            return
        
        if data["phone"] != page.session.get("phone"):
            page.show_snack_bar(ft.SnackBar(ft.Text(f"رسالة من {data['user']}")))

        if not data.get("is_image"):
            with open(DB_FILE, "a", encoding="utf-8") as f:
                f.write(f"{data['user']}|{data['text']}|{data['phone']}\n")
        add_message_to_ui(data['user'], data['text'], data['phone'], data.get("is_image", False))

    page.pubsub.subscribe(on_broadcast)
    msg_input = ft.TextField(hint_text="اكتب رسالة...", expand=True, border_radius=25)

def send_message(e):
        if msg_input.value.strip():
            page.pubsub.send_all({"phone": page.session.get("phone"), "user": page.session.get("username"), "text": msg_input.value})
            msg_input.value = ""
            page.update()

def enter_chat_room():
    page.pubsub.send_all({"action": "login", "phone": page.session.get("phone"), "user": page.session.get("user")})
    page.clean()
    page.appbar = ft.AppBar(
        title=ft.Text("أصيل ميسنجر"),
        bgcolor="gold",
        actions=[ft.IconButton(icon=None, on_click=lambda _: clear_chat_secure(), tooltip="لوحة التحكم")]
    )
page.add(ft.Column([ft.Row([ft.Container(content=chat_list, expand=True)])]))
page.add(ft.Container(content=ft.Row([msg_input, ft.IconButton(icon=None, on_click=send_message)])))
txt_name = ft.TextField(label="الاسم", width=300)
txt_phone = ft.TextField(label="رقم الهاتف", width=300)

page.add(
    ft.Container(
        content=ft.Column([
            ft.ElevatedButton("دخول", on_click=lambda _: enter_chat_room())
        ])
      )
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8000, host="0.0.0.0")

