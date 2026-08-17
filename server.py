from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os


class UltimateBootstrapServer(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/' or self.path == '/index' or self.path == '/index.html':
            self.send_response(200)
            active_tab = 'main'
            content_file = 'templates/main.html'
        elif self.path == '/categories':
            self.send_response(200)
            active_tab = 'categories'
            content_file = 'templates/categories.html'
        elif self.path == '/orders':
            self.send_response(200)
            active_tab = 'orders'
            content_file = 'templates/orders.html'
        elif self.path == '/contacts':
            self.send_response(200)
            active_tab = 'contacts'
            content_file = 'templates/contacts.html'
        else:
            self.send_response(404)
            active_tab = 'none'
            content_file = 'templates/page_404.html'

        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        with open('templates/base_menu.html', 'r', encoding='utf-8') as file:
            base_html = file.read()

        if os.path.exists(content_file):
            with open(content_file, 'r', encoding='utf-8') as file:
                page_content = file.read()
        else:
            page_content = "<h2>Файл шаблона не найден.</h2>"


        final_html = base_html.replace('{{CONTENT}}', page_content)


        final_html = final_html.replace(f'id="nav-{active_tab}" class="nav-link text-white"',
                                        f'id="nav-{active_tab}" class="nav-link active bg-primary text-white"')

        self.wfile.write(final_html.encode('utf-8'))


    def do_POST(self):
        if self.path == '/contacts':
            content_length = int(self.headers['Content-Length'])
            raw_post_data = self.rfile.read(content_length).decode('utf-8')

            # Декодируем параметры формы в словарь
            parsed_data = urllib.parse.parse_qs(raw_post_data)

            print("\n================================================")
            print("=== [POST] ПОЛУЧЕНЫ ДАННЫЕ ИЗ ФОРМЫ КОНТАКТОВ ===")
            print("================================================")
            for key, value in parsed_data.items():
                print(f"Поле '{key}': {value[0] if value else ''}")
            print("================================================\n")

            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()


            success_html = """
            <!DOCTYPE html>
            <html lang="ru">
            <head><meta charset="UTF-8"><link href="https://jsdelivr.net" rel="stylesheet"></head>
            <body class="bg-light d-flex align-items-center justify-content-center vh-100">
                <div class="card p-5 shadow-sm text-center" style="max-width: 500px;">
                    <h2 class="text-success mb-3">✓ Данные успешно приняты!</h2>
                    <p class="text-muted">Все переданные поля формы были успешно напечатаны в консоли вашего Python-сервера.</p>
                    <a href="/contacts" class="btn btn-primary mt-3">Назад к контактам</a>
                </div>
            </body>
            </html>
            """
            self.wfile.write(success_html.encode('utf-8'))


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, UltimateBootstrapServer)
    print("Сервер запущен по адресу: http://localhost:8000")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
