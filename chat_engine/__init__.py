from .mensaje import Mensaje
from datetime import datetime
from shiny import module, ui, Session, reactive, req

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
                style_ = "width: 100%; height: 50vh; border: solid 1px black; overflow-y: scroll; display:flex; flex-direction: column-reverse;"
            ),
            ui.tags.br(),
            ui.input_text(
                id = "nombre",
                label = None,
                value = "",
                placeholder = "Tu nombre...",
                width = "100%"
            ),
            ui.input_text_area(
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
def chat_server(input, output, session: Session, chat_engine: ChatEngine):
    @reactive.poll(chat_engine.get_index, 0.5)
    def get_index() -> int:
        return(chat_engine.get_index())

    index_actual = reactive.Value(chat_engine.get_index())

    for mensaje in chat_engine.get_mensajes(from_ = 0):
        ui.insert_ui(
            selector= "#" + chat_engine.id_,
            immediate=True,
            where = "afterBegin",
            ui = ui.TagList(
                ui.p(mensaje.format())
            )
        )

    @reactive.Effect
    @reactive.event(get_index)
    def actualizar_mensajes():
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
        ui.update_text_area(
            id = "mensaje",
            value=""
        )

    @reactive.Effect
    @reactive.event(input.enviar)
    def enviar_mensaje():
        req(input.nombre())
        req(input.mensaje())
        chat_engine.enviar_mensaje(emisor = input.nombre(), contenido = input.mensaje())


