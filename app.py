from shiny import App, ui, Session, reactive, req
from chat_engine import chat_ui, chat_server, ChatEngine

chat_engine_c1 = ChatEngine("c1")
chat_engine_c2 = ChatEngine("c2")

app_ui = ui.page_navbar(
    ui.nav(
        "Chat 1",
        chat_ui("chat1", chat_engine_c1)
    ),
    ui.nav(
        "Chat 2",
        chat_ui("chat2", chat_engine_c2)
    ),
    title = "Mi Chat"
)


def server(input, output, session: Session):
    chat_server("chat1", chat_engine_c1)
    chat_server("chat2", chat_engine_c2)

app = App(app_ui, server)
