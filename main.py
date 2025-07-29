import os
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Определяем корневую директорию проекта
            root_dir = os.path.dirname(os.path.abspath(__file__))

            # Если запрошен корневой путь, показываем contacts.html
            if self.path == '/':
                self.path = '/html_pages/contacts.html'

            # Получаем полный путь к запрошенному файлу
            file_path = os.path.join(root_dir, self.path.lstrip('/'))

            # Определяем MIME-тип файла
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/octet-stream'

            # Читаем и отправляем файл
            if os.path.exists(file_path):
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()

                # Для текстовых файлов используем текстовое чтение
                if content_type.startswith(('text/', 'application/javascript')):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.wfile.write(content.encode('utf-8'))
                else:
                    # Для бинарных файлов используем бинарное чтение
                    with open(file_path, 'rb') as f:
                        self.wfile.write(f.read())
            else:
                # Если файл не найден
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'404 Not Found')

        except Exception as e:
            print(f"Ошибка при обработке запроса: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"Внутренняя ошибка сервера: {str(e)}".encode('utf-8'))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Сервер запущен http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Сервер остановлен.")