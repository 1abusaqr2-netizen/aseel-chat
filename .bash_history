cat main.py
lt --port 8502
python main.py
pkg install cloudflared -y
cloudflared tunnel --url http://127.0.0.1:8502
import flet as ft
import random
import os
def main(page: ft.Page):
# تشغيل التطبيق بنمط الويب للسيرفرات
if __name__ == "__main__":;     port = int(os.getenv("PORT", 8080))
cat <<EOF > main.py
import flet as ft
import random
import os

def main(page: ft.Page):
    page.title = "نظام م/ اصيل السبعي المراسلة العالمي"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.LIGHT
    generated_otp = None

    txt_name = ft.TextField(label="الاسم المستعار")
    txt_phone = ft.TextField(label="رقم الهاتف")
    txt_otp = ft.TextField(label="كود التحقق", visible=False)
    chat_list = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    msg_input = ft.TextField(hint_text="اكتب رسالة...", expand=True)

    def on_broadcast(data):
        is_me = data["phone"] == page.session.get("phone")
        chat_list.controls.append(
            ft.Container(
                content=ft.Text(f"{data['user']}: {data['text']}"),
                bgcolor="#E1FFC7" if is_me else "#F0F0F0",
                padding=10, border_radius=10,
                alignment=ft.alignment.center_right if is_me else ft.alignment.center_left
            )
        )
        page.update()

    page.pubsub.subscribe(on_broadcast)

    def send_message(e):
        if msg_input.value:
            page.pubsub.send_all({
                "phone": page.session.get("phone"),
                "user": page.session.get("username"),
                "text": msg_input.value
            })
            msg_input.value = ""
            page.update()

    def verify_logic(e):
        nonlocal generated_otp
        if not txt_otp.visible:
            generated_otp = str(random.randint(1000, 9999))
            page.snack_bar = ft.SnackBar(ft.Text(f"كود التحقق هو: {generated_otp}"), open=True)
            txt_otp.visible = True
            btn_login.text = "تأكيد الدخول"
            page.update()
        else:
            if txt_otp.value == generated_otp:
                page.session.set("phone", txt_phone.value)
                page.session.set("username", txt_name.value or "مستخدم")
                show_chat()
            else:
                txt_otp.error_text = "الكود خاطئ"
                page.update()

    def show_chat():
        page.clean()
        page.add(ft.AppBar(title=ft.Text("دردشة عامة"), bgcolor="gold"), chat_list, ft.Row([msg_input, ft.IconButton(ft.icons.SEND, on_click=send_message)]))

    btn_login = ft.ElevatedButton("طلب كود التحقق", on_click=verify_logic)
    page.add(ft.Column([txt_name, txt_phone, txt_otp, btn_login], horizontal_alignment="center"))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8502))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
EOF

python main.py
apt update -y
