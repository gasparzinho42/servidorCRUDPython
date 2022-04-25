import sys
import cgi
from http.server import HTTPServer, SimpleHTTPRequestHandler
from database.database import create_table, insert_record, fetch_records,update_table,delete_record

HOST_NAME = "localhost"
PORT = 8080


def read_html_template(path):
    """funcao para ler arquivo html"""
    try:
        with open(path) as f:
            file = f.read()
    except Exception as e:
        file = e
    return file


def show_records(self):
    """funcao para mostrar registros no modelo"""
    file = read_html_template(self.path)
    tableData = fetch_records()
    tableRow = ""
    for data in tableData:
        print(f" tableData => {data}")
        tableRow += "<tr>"
        for item in data:
            tableRow += "<td>"
            tableRow += str(item)
            tableRow += "</td>"
        tableRow += "</tr>"
    file = file.replace("{{user_records}}", tableRow)
    self.send_response(200, "OK")
    self.end_headers()
    self.wfile.write(bytes(file, "UTF-8"))


class PythonServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'templates/form/index.html'
            file = read_html_template(self.path)
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(bytes(file, "UTF-8"))
        if self.path == '/show_records':
            self.path = 'templates/showRecords/index.html'
            show_records(self)

    def do_POST(self):
        if self.path == '/success':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'UTF-8')

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                full_name = fields.get('full_name')[0]
                country = fields.get('country')[0]

                create_table()

                insert_record(full_name, country)

                html = f"<html><head></head><body><h1>Dados do formulario gravados com sucesso!!!</h1><br><a href='/'>Formulario</a></body></html>"
                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes(html, 'UTF-8'))
        if self.path == '/update':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'UTF-8')
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                item_id = fields.get('item_id')[0]
                full_name = fields.get('full_name_update')[0]
                country = fields.get('country_update')[0]
                update_table(item_id, full_name, country)
                html = f"<html><head></head><body><h1>Dados do formulario atualizados com sucesso!!!</h1><br><a href='/'>Formulario</a></body></html>"
                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes(html, 'utf-8'))
        if self.path == '/delete':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'UTF-8')
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                item_id = fields.get('item_id')[0]
                delete_record(item_id)
                html = f"<html><head></head><body><h1>Dado do formulario deletado com sucesso!!!</h1><br><a href='/'>Formulario</a></body></html>"
                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes(html, 'UTF-8'))

if __name__ == "__main__":
    server = HTTPServer((HOST_NAME,PORT), PythonServer)
    print(f"Servidor iniciado http://{HOST_NAME}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Servidor parado com sucesso")
        sys.exit(0)