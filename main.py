import mimetypes
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    """Специальный класс, который отвечает за обработку входящих запросов от клиентов"""

    def do_GET(self):
        """Метод для обработки входящих GET-запросов"""
        try:
            # Определяем корневую директорию проекта
            root_dir = os.path.dirname(os.path.abspath(__file__))

            # Если запрошен корневой путь, показываем contacts.html
            if self.path == "/":
                self.path = "/html_pages/contacts.html"

            # Получаем полный путь к запрошенному файлу
            file_path = os.path.join(root_dir, self.path.lstrip("/"))

            # Определяем MIME-тип файла
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = "application/octet-stream"

            # Читаем и отправляем файл
            if os.path.exists(file_path):
                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.end_headers()

                # Для текстовых файлов используем текстовое чтение
                if content_type.startswith(("text/", "application/javascript")):
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        self.wfile.write(content.encode("utf-8"))
                else:
                    # Для бинарных файлов используем бинарное чтение
                    with open(file_path, "rb") as f:
                        self.wfile.write(f.read())
            else:
                # Если файл не найден
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"404 Not Found")

        except Exception as e:
            print(f"Ошибка при обработке запроса: {e}")
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"Внутренняя ошибка сервера: {str(e)}".encode("utf-8"))

    def do_POST(self):
        """Метод для обработки входящих POST-запросов"""
        try:
            # Получаем длину тела запроса
            content_length = int(self.headers["Content-Length"])

            # Читаем тело запроса
            post_data = self.rfile.read(content_length).decode("utf-8")

            # Выводим данные в консоль
            print("Получены данные от пользователя:")

            # Разбираем данные формы
            form_data = {}
            for pair in post_data.split("&"):
                key, value = pair.split("=")
                # Декодируем URL-encoded строку
                from urllib.parse import unquote

                form_data[unquote(key)] = unquote(value)

            # Выводим в консоль в удобном формате
            print(f"Имя: {form_data.get('name', '')}")
            print(f"Email: {form_data.get('email', '')}")
            print(f"Сообщение: {form_data.get('message', '')}")

            # Отправляем ответ пользователю
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            # Отправляем простое подтверждение
            response = """
            <html>
                <head>
                    <meta charset="utf-8">
                    <meta http-equiv="refresh" content="3;url=/html_pages/contacts.html">
                </head>
                <body>
                    <h1>Сообщение успешно отправлено!</h1>
                    <p>Вы будете перенаправлены обратно через 3 секунды...</p>
                </body>
            </html>
            """.encode(
                "utf-8"
            )

            self.wfile.write(response)

        except Exception as e:
            print(f"Ошибка при обработке POST-запроса: {e}")
            self.send_response(500)
            self.end_headers()


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Сервер запущен http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Сервер остановлен.")
