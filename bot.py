import discord
from discord import app_commands
import json
import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

load_dotenv()  # lee las variables del archivo .env

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Pon aquí el ID de tu servidor para que los comandos aparezcan al instante
# mientras pruebas (clic derecho al ícono del servidor > Copiar ID de servidor,
# necesitas el "Modo desarrollador" activado en Discord).
GUILD_ID = None  # ejemplo: 123456789012345678

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ── Sistema de idiomas ─────────────────────────────────────
IDIOMA_FILE = "idioma_data.json"


def cargar_idiomas() -> dict:
    if not os.path.exists(IDIOMA_FILE):
        return {}
    with open(IDIOMA_FILE, "r", encoding="utf-8") as f:
        # las claves se guardan como texto en JSON, las convertimos a int
        return {int(k): v for k, v in json.load(f).items()}


def guardar_idiomas(data: dict) -> None:
    with open(IDIOMA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


idioma_servidor = cargar_idiomas()

TEXTOS = {
    "es": {
        "reglas_ok": "✅ Mensaje enviado en {canal}",
        "kick_ok": "👢 **{usuario}** fue expulsado. Razón: {razon}",
        "kick_sin_permisos": "❌ No pude expulsar a ese usuario. Revisa que el rol de mi bot esté más arriba que el del usuario en Configuración del servidor > Roles.",
        "xp_ok": "✨ **{usuario}** ahora tiene **{total}** XP ({signo}{cantidad}).",
        "nivel_ok": "📊 **{usuario}** tiene **{xp}** XP.",
        "sin_permiso": "❌ No tienes permisos para usar este comando.",
        "bienvenida_titulo": "👋 ¡Bienvenido a {servidor}!",
        "bienvenida_desc": "Hola {usuario}, gracias por unirte. Recuerda leer las reglas del servidor para que todo vaya bien.",
        "rol_ok": "✅ Se le dio el rol **{rol}** a **{usuario}**.",
        "rol_ya_tiene": "⚠️ **{usuario}** ya tiene el rol **{rol}**.",
        "rol_sin_permisos": "❌ No pude darle ese rol. Revisa que el rol de mi bot esté más arriba que el rol que intento asignar, en Configuración del servidor > Roles.",
        "malapalabra_titulo": "⚠️ Advertencia — Mala palabra detectada",
        "malapalabra_usuario": "Usuario",
        "malapalabra_canal": "Canal",
        "malapalabra_palabra": "Palabra detectada",
        "malapalabra_mensaje": "Mensaje original",
        "malapalabra_aviso_usuario": "🚫 {usuario}, tu mensaje fue eliminado por contener lenguaje ofensivo.",
        "traducir_error": "❌ No pude traducir ese texto. Intenta de nuevo.",
        "apply_iniciado": "📬 Te envié la postulación por mensaje privado, revisa tus DMs.",
        "apply_dm_cerrado": "❌ No pude enviarte un mensaje privado. Activa los DMs para este servidor e inténtalo de nuevo.",
        "apply_ya_activa": "⚠️ Ya tienes una postulación en curso, revisa tus DMs.",
        "apply_timeout": "⌛ Se acabó el tiempo para responder. Usa /apply de nuevo si quieres intentarlo otra vez.",
        "apply_intro": "📋 **Postulación para Staff**\nTe voy a hacer {n} preguntas, una por una. Responde cada una con un mensaje normal. Tienes 10 minutos por pregunta.",
        "apply_final": "✅ ¡Listo! Tu postulación fue enviada al staff. Te avisarán pronto.",
        "apply_enviada_canal": "📥 Nueva postulación de {usuario}",
        "idioma_cambiado": "✅ Idioma del bot cambiado a **Español** 🇪🇸",
        "apply_panel_titulo": "📋 Postulación para Staff",
        "apply_panel_desc": "¿Quieres unirte al equipo de Staff? Dale clic al botón de abajo y te vamos a hacer algunas preguntas por mensaje privado.",
        "apply_panel_boton": "📋 Aplicar a Staff",
        "apply_aceptado_dm": "🎉 ¡Felicidades! Tu postulación para Staff en **{servidor}** fue **aceptada**.",
        "apply_rechazado_dm": "📪 Tu postulación para Staff en **{servidor}** fue **rechazada** esta vez. ¡Gracias por tu interés!",
        "apply_aceptado_canal": "✅ Aceptado por {staff}",
        "apply_rechazado_canal": "❌ Rechazado por {staff}",
        "apply_sin_permiso_revision": "❌ No tienes permisos para revisar postulaciones.",
        "apply_rol_no_configurado": "⚠️ Se aceptó, pero no pude asignar el rol (revisa ROL_STAFF_ID en el código).",
    },
    "en": {
        "reglas_ok": "✅ Message sent in {canal}",
        "kick_ok": "👢 **{usuario}** was kicked. Reason: {razon}",
        "kick_sin_permisos": "❌ I couldn't kick that user. Make sure my bot's role is above the user's role in Server Settings > Roles.",
        "xp_ok": "✨ **{usuario}** now has **{total}** XP ({signo}{cantidad}).",
        "nivel_ok": "📊 **{usuario}** has **{xp}** XP.",
        "sin_permiso": "❌ You don't have permission to use this command.",
        "bienvenida_titulo": "👋 Welcome to {servidor}!",
        "bienvenida_desc": "Hi {usuario}, thanks for joining. Make sure to read the server rules so everything goes smoothly.",
        "rol_ok": "✅ Gave the **{rol}** role to **{usuario}**.",
        "rol_ya_tiene": "⚠️ **{usuario}** already has the **{rol}** role.",
        "rol_sin_permisos": "❌ I couldn't assign that role. Make sure my bot's role is above the role I'm trying to assign, in Server Settings > Roles.",
        "malapalabra_titulo": "⚠️ Warning — Bad word detected",
        "malapalabra_usuario": "User",
        "malapalabra_canal": "Channel",
        "malapalabra_palabra": "Detected word",
        "malapalabra_mensaje": "Original message",
        "malapalabra_aviso_usuario": "🚫 {usuario}, your message was removed for containing offensive language.",
        "traducir_error": "❌ I couldn't translate that text. Try again.",
        "apply_iniciado": "📬 I sent you the application by DM, check your messages.",
        "apply_dm_cerrado": "❌ I couldn't send you a DM. Enable DMs for this server and try again.",
        "apply_ya_activa": "⚠️ You already have an application in progress, check your DMs.",
        "apply_timeout": "⌛ Time's up to answer. Use /apply again if you want to try once more.",
        "apply_intro": "📋 **Staff Application**\nI'll ask you {n} questions, one at a time. Reply with a normal message. You have 10 minutes per question.",
        "apply_final": "✅ Done! Your application was sent to staff. They'll get back to you soon.",
        "apply_enviada_canal": "📥 New application from {usuario}",
        "idioma_cambiado": "✅ Bot language changed to **English** 🇬🇧",
        "apply_panel_titulo": "📋 Staff Application",
        "apply_panel_desc": "Want to join the Staff team? Click the button below and we'll ask you a few questions by DM.",
        "apply_panel_boton": "📋 Apply for Staff",
        "apply_aceptado_dm": "🎉 Congrats! Your Staff application for **{servidor}** was **accepted**.",
        "apply_rechazado_dm": "📪 Your Staff application for **{servidor}** was **rejected** this time. Thanks for your interest!",
        "apply_aceptado_canal": "✅ Accepted by {staff}",
        "apply_rechazado_canal": "❌ Rejected by {staff}",
        "apply_sin_permiso_revision": "❌ You don't have permission to review applications.",
        "apply_rol_no_configurado": "⚠️ Accepted, but I couldn't assign the role (check ROL_STAFF_ID in the code).",
    },
    "pt": {
        "reglas_ok": "✅ Mensagem enviada em {canal}",
        "kick_ok": "👢 **{usuario}** foi expulso. Motivo: {razon}",
        "kick_sin_permisos": "❌ Não consegui expulsar esse usuário. Verifique se o cargo do meu bot está acima do cargo do usuário em Configurações do servidor > Cargos.",
        "xp_ok": "✨ **{usuario}** agora tem **{total}** XP ({signo}{cantidad}).",
        "nivel_ok": "📊 **{usuario}** tem **{xp}** XP.",
        "sin_permiso": "❌ Você não tem permissão para usar este comando.",
        "bienvenida_titulo": "👋 Bem-vindo(a) a {servidor}!",
        "bienvenida_desc": "Olá {usuario}, obrigado por entrar. Não esqueça de ler as regras do servidor.",
        "rol_ok": "✅ O cargo **{rol}** foi dado a **{usuario}**.",
        "rol_ya_tiene": "⚠️ **{usuario}** já tem o cargo **{rol}**.",
        "rol_sin_permisos": "❌ Não consegui dar esse cargo. Verifique se o cargo do meu bot está acima do cargo que estou tentando atribuir, em Configurações do servidor > Cargos.",
        "malapalabra_titulo": "⚠️ Aviso — Palavra ofensiva detectada",
        "malapalabra_usuario": "Usuário",
        "malapalabra_canal": "Canal",
        "malapalabra_palabra": "Palavra detectada",
        "malapalabra_mensaje": "Mensagem original",
        "malapalabra_aviso_usuario": "🚫 {usuario}, sua mensagem foi removida por conter linguagem ofensiva.",
        "traducir_error": "❌ Não consegui traduzir esse texto. Tente novamente.",
        "apply_iniciado": "📬 Enviei a candidatura para o seu privado, confira suas DMs.",
        "apply_dm_cerrado": "❌ Não consegui te enviar uma DM. Ative as DMs para este servidor e tente novamente.",
        "apply_ya_activa": "⚠️ Você já tem uma candidatura em andamento, confira suas DMs.",
        "apply_timeout": "⌛ O tempo para responder acabou. Use /apply novamente se quiser tentar outra vez.",
        "apply_intro": "📋 **Candidatura para Staff**\nVou fazer {n} perguntas, uma de cada vez. Responda com uma mensagem normal. Você tem 10 minutos por pergunta.",
        "apply_final": "✅ Pronto! Sua candidatura foi enviada para o staff. Em breve entrarão em contato.",
        "apply_enviada_canal": "📥 Nova candidatura de {usuario}",
        "idioma_cambiado": "✅ Idioma do bot alterado para **Português** 🇧🇷",
        "apply_panel_titulo": "📋 Candidatura para Staff",
        "apply_panel_desc": "Quer entrar para a equipe de Staff? Clique no botão abaixo e vamos te fazer algumas perguntas por DM.",
        "apply_panel_boton": "📋 Candidatar-se a Staff",
        "apply_aceptado_dm": "🎉 Parabéns! Sua candidatura para Staff em **{servidor}** foi **aceita**.",
        "apply_rechazado_dm": "📪 Sua candidatura para Staff em **{servidor}** foi **rejeitada** desta vez. Obrigado pelo interesse!",
        "apply_aceptado_canal": "✅ Aceito por {staff}",
        "apply_rechazado_canal": "❌ Rejeitado por {staff}",
        "apply_sin_permiso_revision": "❌ Você não tem permissão para revisar candidaturas.",
        "apply_rol_no_configurado": "⚠️ Aceito, mas não consegui atribuir o cargo (verifique ROL_STAFF_ID no código).",
    },
}


def t(guild_id, clave, **kwargs):
    lang = idioma_servidor.get(guild_id, "es")
    texto = TEXTOS[lang].get(clave, TEXTOS["es"].get(clave, clave))
    return texto.format(**kwargs) if kwargs else texto


@client.event
async def on_ready():
    client.add_view(PanelApplyView())  # para que el botón siga funcionando tras reiniciar
    client.add_view(RevisionApplyView())  # botones de aceptar/rechazar postulaciones

    if GUILD_ID:
        guild = discord.Object(id=GUILD_ID)
        tree.copy_global_to(guild=guild)
        await tree.sync(guild=guild)  # instantáneo, solo en ese servidor
    else:
        await tree.sync()  # global, puede tardar hasta 1 hora en aparecer

    print(f"✅ Bot conectado como: {client.user}")


# ── Traducción automática por canal (vía webhook) ────────────
# Pon aquí el nombre exacto del canal y a qué idioma quieres que
# se traduzca todo lo que se escriba ahí. Ejemplo:
# CANALES_TRADUCCION = {"chat": "en", "general": "es"}
CANALES_TRADUCCION = {
    # "chat": "en",
}

_webhooks_cache = {}


async def obtener_webhook(canal: discord.TextChannel) -> discord.Webhook:
    if canal.id in _webhooks_cache:
        return _webhooks_cache[canal.id]

    webhooks = await canal.webhooks()
    webhook = discord.utils.get(webhooks, name="traductor-bot")
    if webhook is None:
        webhook = await canal.create_webhook(name="traductor-bot")

    _webhooks_cache[canal.id] = webhook
    return webhook


async def traducir_y_reenviar(message: discord.Message, idioma_destino: str):
    try:
        traduccion = GoogleTranslator(source="auto", target=idioma_destino).translate(message.content)
    except Exception:
        return

    # Si ya está en el idioma destino, la traducción sale igual: no hacemos nada.
    if traduccion.strip().lower() == message.content.strip().lower():
        return

    try:
        await message.delete()
    except discord.Forbidden:
        return

    try:
        webhook = await obtener_webhook(message.channel)
        await webhook.send(
            content=traduccion,
            username=message.author.display_name,
            avatar_url=message.author.display_avatar.url,
        )
    except discord.Forbidden:
        pass


# ── Anti malas palabras (inglés) ─────────────────────────────
import re

MALAS_PALABRAS = [
    "fuck", "shit", "bitch", "asshole", "bastard", "cunt", "dick",
    "piss", "slut", "whore", "faggot", "nigger", "retard",
]
PATRON_MALAS_PALABRAS = re.compile(
    r"\b(" + "|".join(re.escape(p) for p in MALAS_PALABRAS) + r")\b",
    re.IGNORECASE,
)

NOMBRE_CANAL_ADVERTENCIAS = "advertencias"


def contiene_mala_palabra(texto: str):
    coincidencia = PATRON_MALAS_PALABRAS.search(texto)
    return coincidencia.group(0) if coincidencia else None


@client.event
async def on_message(message: discord.Message):
    if message.author.bot or not message.guild:
        return

    # ── Traducción automática (si el canal está configurado) ──
    idioma_destino = CANALES_TRADUCCION.get(message.channel.name)
    if idioma_destino:
        await traducir_y_reenviar(message, idioma_destino)
        return  # el mensaje original ya se borró y se reenvió traducido

    palabra_detectada = contiene_mala_palabra(message.content)
    if palabra_detectada:
        gid = message.guild.id
        contenido_original = message.content
        canal_origen = message.channel

        try:
            await message.delete()
        except discord.Forbidden:
            pass

        try:
            await message.channel.send(
                t(gid, "malapalabra_aviso_usuario", usuario=message.author.mention),
                delete_after=6,
            )
        except discord.Forbidden:
            pass

        canal_advertencias = discord.utils.get(
            message.guild.text_channels, name=NOMBRE_CANAL_ADVERTENCIAS
        )
        if canal_advertencias:
            embed = discord.Embed(
                title=t(gid, "malapalabra_titulo"),
                color=discord.Color.orange(),
            )
            embed.add_field(name=t(gid, "malapalabra_usuario"), value=message.author.mention, inline=True)
            embed.add_field(name=t(gid, "malapalabra_canal"), value=canal_origen.mention, inline=True)
            embed.add_field(name=t(gid, "malapalabra_palabra"), value=f"`{palabra_detectada}`", inline=True)
            embed.add_field(name=t(gid, "malapalabra_mensaje"), value=contenido_original[:1000], inline=False)
            try:
                await canal_advertencias.send(embed=embed)
            except discord.Forbidden:
                pass


# ── Bienvenida por privado (DM) ─────────────────────────────
@client.event
async def on_member_join(usuario: discord.Member):
    embed = discord.Embed(
        title=f"👋 ¡Bienvenido a {usuario.guild.name}! / Welcome to {usuario.guild.name}!",
        color=discord.Color.green(),
    )
    embed.add_field(
        name="🇪🇸 Español",
        value=f"Hola {usuario.mention}, gracias por unirte. Recuerda leer las reglas del servidor para que todo vaya bien.",
        inline=False,
    )
    embed.add_field(
        name="🇬🇧 English",
        value=f"Hi {usuario.mention}, thanks for joining. Make sure to read the server rules so everything goes smoothly.",
        inline=False,
    )
    if usuario.guild.icon:
        embed.set_thumbnail(url=usuario.guild.icon.url)

    try:
        await usuario.send(embed=embed)
    except discord.Forbidden:
        # El usuario tiene los DMs cerrados para ese servidor/bot, no se puede hacer nada.
        pass


# ── XP: almacenamiento en JSON ──────────────────────────────
XP_FILE = "xp_data.json"


def cargar_xp() -> dict:
    if not os.path.exists(XP_FILE):
        return {}
    with open(XP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_xp(data: dict) -> None:
    with open(XP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ── /traducir ────────────────────────────────────────────────
IDIOMAS_DISPONIBLES = [
    app_commands.Choice(name="Español", value="es"),
    app_commands.Choice(name="Inglés", value="en"),
    app_commands.Choice(name="Portugués", value="pt"),
    app_commands.Choice(name="Francés", value="fr"),
    app_commands.Choice(name="Italiano", value="it"),
    app_commands.Choice(name="Alemán", value="de"),
]


@tree.command(name="traducir", description="Traduce un texto al idioma que elijas")
@app_commands.describe(
    texto="El texto que quieres traducir",
    idioma="Idioma al que quieres traducirlo",
)
@app_commands.choices(idioma=IDIOMAS_DISPONIBLES)
async def traducir(interaction: discord.Interaction, texto: str, idioma: app_commands.Choice[str]):
    gid = interaction.guild.id if interaction.guild else None
    await interaction.response.defer()

    try:
        traduccion = GoogleTranslator(source="auto", target=idioma.value).translate(texto)
        await interaction.followup.send(traduccion)
    except Exception:
        await interaction.followup.send(t(gid, "traducir_error"), ephemeral=True)


# ── /idioma ──────────────────────────────────────────────────
@tree.command(name="idioma", description="Cambia el idioma en el que responde el bot en este servidor")
@app_commands.checks.has_permissions(manage_guild=True)
@app_commands.describe(idioma="Idioma que quieres que use el bot")
@app_commands.choices(idioma=[
    app_commands.Choice(name="Español", value="es"),
    app_commands.Choice(name="English", value="en"),
    app_commands.Choice(name="Português", value="pt"),
])
async def idioma(interaction: discord.Interaction, idioma: app_commands.Choice[str]):
    gid = interaction.guild.id
    idioma_servidor[gid] = idioma.value
    guardar_idiomas(idioma_servidor)
    await interaction.response.send_message(t(gid, "idioma_cambiado"))


# ── /apply (panel de postulación de staff) ───────────────────
CANAL_POSTULACIONES = "postulaciones"  # nombre exacto del canal donde llegan las respuestas
ROL_STAFF_ID = 1523542959302115336  # rol que se le da al aceptar una postulación

PREGUNTAS_APPLY = {
    "es": [
        "👤 **Información Personal**\n1️⃣ ¿Cuál es tu nombre de usuario en Discord?",
        "2️⃣ ¿Qué edad tienes?",
        "3️⃣ ¿Cuál es tu zona horaria?",
        "4️⃣ ¿Cuántas horas al día puedes dedicar al servidor?",
        "💼 **Experiencia**\n5️⃣ ¿Has sido Staff en otros servidores de Discord? Si tu respuesta es sí, incluye en el mismo mensaje: nombre del servidor, cargo que ocupabas, tiempo que estuviste y motivo por el que dejaste el cargo. Si no, responde 'No'.",
        "6️⃣ ¿Has administrado un servidor propio?",
        "7️⃣ ¿Qué bots sabes utilizar? (Dyno, Carl-bot, Ticket Tool, MEE6, Sapphire, etc.)",
        "8️⃣ ¿Sabes configurar permisos, roles y canales? Explica tu nivel de experiencia.",
        "📚 **Conocimientos**\n9️⃣ ¿Cuál es la función de un Moderador?",
        "🔟 ¿Cuál es la diferencia entre un Moderador y un Administrador?",
        "1️⃣1️⃣ ¿Qué harías antes de banear a un usuario?",
        "1️⃣2️⃣ ¿Qué es el abuso de permisos?",
    ],
    "en": [
        "👤 **Personal Information**\n1️⃣ What is your Discord username?",
        "2️⃣ How old are you?",
        "3️⃣ What is your timezone?",
        "4️⃣ How many hours a day can you dedicate to the server?",
        "💼 **Experience**\n5️⃣ Have you been Staff on other Discord servers? If yes, include in the same message: server name, role you held, how long you were there, and why you left. If not, answer 'No'.",
        "6️⃣ Have you managed your own server?
