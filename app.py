from shiny import App, ui, Session, reactive, req, Outputs, Inputs
from chat_engine import chat_ui, chat_server, ChatEngine
from htmltools import HTMLDependency

chat_engine_c1 = ChatEngine("chat1")
chat_engine_c2 = ChatEngine("chat2")

app_ui = ui.TagList(
    ui.tags.head(
        HTMLDependency(
            name = "main",
            version = "1.0",
            source = { "subdir": "html_deps/main" },
            stylesheet = { "href": "main.css" },
            script = { "src": "main.js" }
        )
    ),
    ui.page_navbar(
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
)


def server(input: Inputs, output: Outputs, session: Session) -> None:
    chat_server("chat1", chat_engine_c1)
    chat_server("chat2", chat_engine_c2)

app = App(app_ui, server)
