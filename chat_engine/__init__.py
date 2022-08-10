from .mensaje import Mensaje
from datetime import datetime
from shiny import module, ui, Session, reactive, req, Inputs, Outputs

class ChatEngine:
    def __init__(self, id_: str) -> None:
        self.id_ = id_
        self.index: int = 0
        self.mensajes: list[Mensaje] = []
    def enviar_mensaje(self, emisor: str, contenido: str) -> None:
        if len(contenido) > 75:
            contenido = contenido[0:75] + "..."
        mensaje = Mensaje(emisor=emisor, contenido=contenido, hora = datetime.now())
        self.mensajes.append(mensaje)
        self.index += 1
    def get_index(self) -> int:
        return(self.index)
    def get_mensajes(self, from_: int) -> list[Mensaje]:
        return(self.mensajes[from_:self.index + 1])

@module.ui
def chat_ui(chat_engine: ChatEngine) -> ui.TagChildArg:
    mod_ui = ui.page_fluid(
        ui.column(
            12,
            ui.div(
                id_ = chat_engine.id_,
                class_ = "chat_box border"
            ),
            ui.tags.br(),
            ui.input_text(
                id = "nombre",
                label = None,
                value = "",
                placeholder = "Tu nombre...",
                width = "100%"
            ),
            ui.input_text(
                id = "mensaje",
                label = None,
                value = "",
                placeholder = "Tu mensaje...",
                width = "100%"
            ),
            ui.input_action_button(id = "enviar", label = "Enviar")
        )
    )
    return(mod_ui)

@module.server
def chat_server(input: Inputs, output: Outputs, session: Session, chat_engine: ChatEngine) -> None:

    id_ = chat_engine.id_

    @reactive.poll(chat_engine.get_index, 0.5)
    def get_index() -> int:
        return(chat_engine.get_index())

    index_actual = reactive.Value(chat_engine.get_index())

    ui.run_js(f"bind_chatbox(\"{id_}\")")
    for mensaje in chat_engine.get_mensajes(from_ = 0):
        ui.insert_ui(
            selector= "#" + id_,
            immediate=True,
            where = "afterBegin",
            ui = ui.TagList(
                ui.p(mensaje.format())
            )
        )


    @reactive.Effect
    @reactive.event(get_index)
    def actualizar_mensajes() -> None:
        for mensaje in chat_engine.get_mensajes(from_ = index_actual.get()):
            ui.insert_ui(
                selector= "#" + chat_engine.id_,
                immediate=True,
                where = "afterBegin",
                ui = ui.TagList(
                    ui.p(mensaje.format())
                )
            )
        index_actual.set(get_index())


    @reactive.Effect
    @reactive.event(input.enviar)
    def enviar_mensaje() -> None:
        req(input.nombre())
        req(input.mensaje())
        chat_engine.enviar_mensaje(emisor = input.nombre(), contenido = input.mensaje())
        ui.update_text(
            id = "mensaje",
            value=""
        )


