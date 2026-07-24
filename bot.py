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
    },
}


def t(guild_id, clave, **kwargs):
    lang = idioma_servidor.get(guild_id, "es")
    texto = TEXTOS[lang].get(clave, TEXTOS["es"].get(clave, clave))
    return texto.format(**kwargs) if kwargs else texto


@client.event
async def on_ready():
    client.add_view(PanelApplyView())  # para que el botón siga funcionando tras reiniciar

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
        embed = discord.Embed(color=discord.Color.blurple())
        embed.add_field(name="Original", value=texto[:1000], inline=False)
        embed.add_field(name=f"Traducción ({idioma.name})", value=traduccion[:1000], inline=False)
        await interaction.followup.send(embed=embed)
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
        "6️⃣ Have you managed your own server?",
        "7️⃣ Which bots do you know how to use? (Dyno, Carl-bot, Ticket Tool, MEE6, Sapphire, etc.)",
        "8️⃣ Do you know how to configure permissions, roles and channels? Explain your experience level.",
        "📚 **Knowledge**\n9️⃣ What is the role of a Moderator?",
        "🔟 What's the difference between a Moderator and an Administrator?",
        "1️⃣1️⃣ What would you do before banning a user?",
        "1️⃣2️⃣ What is permission abuse?",
    ],
    "pt": [
        "👤 **Informações Pessoais**\n1️⃣ Qual é o seu nome de usuário no Discord?",
        "2️⃣ Quantos anos você tem?",
        "3️⃣ Qual é o seu fuso horário?",
        "4️⃣ Quantas horas por dia você pode dedicar ao servidor?",
        "💼 **Experiência**\n5️⃣ Você já foi Staff em outros servidores do Discord? Se sim, inclua na mesma mensagem: nome do servidor, cargo que ocupava, tempo que ficou e motivo pelo qual saiu. Se não, responda 'Não'.",
        "6️⃣ Você já administrou um servidor próprio?",
        "7️⃣ Quais bots você sabe usar? (Dyno, Carl-bot, Ticket Tool, MEE6, Sapphire, etc.)",
        "8️⃣ Você sabe configurar permissões, cargos e canais? Explique seu nível de experiência.",
        "📚 **Conhecimentos**\n9️⃣ Qual é a função de um Moderador?",
        "🔟 Qual é a diferença entre um Moderador e um Administrador?",
        "1️⃣1️⃣ O que você faria antes de banir um usuário?",
        "1️⃣2️⃣ O que é abuso de permissões?",
    ],
}

_aplicaciones_activas = set()


async def iniciar_postulacion(interaction: discord.Interaction):
    gid = interaction.guild.id
    guild = interaction.guild
    usuario = interaction.user

    if usuario.id in _aplicaciones_activas:
        await interaction.response.send_message(t(gid, "apply_ya_activa"), ephemeral=True)
        return

    try:
        canal_dm = await usuario.create_dm()
        preguntas = PREGUNTAS_APPLY.get(idioma_servidor.get(gid, "es"), PREGUNTAS_APPLY["es"])
        await canal_dm.send(t(gid, "apply_intro", n=len(preguntas)))
    except discord.Forbidden:
        await interaction.response.send_message(t(gid, "apply_dm_cerrado"), ephemeral=True)
        return

    await interaction.response.send_message(t(gid, "apply_iniciado"), ephemeral=True)

    _aplicaciones_activas.add(usuario.id)
    respuestas = []

    def check(m: discord.Message):
        return m.author.id == usuario.id and isinstance(m.channel, discord.DMChannel)

    try:
        for pregunta in preguntas:
            await canal_dm.send(pregunta)
            try:
                respuesta = await client.wait_for("message", check=check, timeout=600)
                respuestas.append(respuesta.content)
            except Exception:
                await canal_dm.send(t(gid, "apply_timeout"))
                return

        await canal_dm.send(t(gid, "apply_final"))

        canal_postulaciones = discord.utils.get(guild.text_channels, name=CANAL_POSTULACIONES)
        if canal_postulaciones:
            embed = discord.Embed(
                title=t(gid, "apply_enviada_canal", usuario=str(usuario)),
                color=discord.Color.blurple(),
            )
            if usuario.display_avatar:
                embed.set_thumbnail(url=usuario.display_avatar.url)
            for pregunta, respuesta in zip(preguntas, respuestas):
                pregunta_limpia = pregunta.split("\n")[-1]
                embed.add_field(name=pregunta_limpia[:256], value=respuesta[:1000] or "-", inline=False)
            await canal_postulaciones.send(embed=embed)
    finally:
        _aplicaciones_activas.discard(usuario.id)


class PanelApplyView(discord.ui.View):
    def __init__(self, etiqueta_boton="📋 Aplicar a Staff"):
        super().__init__(timeout=None)
        self.boton_aplicar.label = etiqueta_boton

    @discord.ui.button(style=discord.ButtonStyle.blurple, custom_id="panel_apply_boton")
    async def boton_aplicar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await iniciar_postulacion(interaction)


@tree.command(name="apply", description="Publica el panel para que la gente aplique a Staff")
@app_commands.checks.has_permissions(manage_guild=True)
async def apply(interaction: discord.Interaction):
    gid = interaction.guild.id
    embed = discord.Embed(
        title=t(gid, "apply_panel_titulo"),
        description=t(gid, "apply_panel_desc"),
        color=discord.Color.blurple(),
    )
    if interaction.guild.icon:
        embed.set_thumbnail(url=interaction.guild.icon.url)

    await interaction.response.send_message(embed=embed, view=PanelApplyView(t(gid, "apply_panel_boton")))


# ── /reglas ──────────────────────────────────────────────────
@tree.command(name="reglas", description="Envía un mensaje/reglas a un canal elegido")
@app_commands.checks.has_permissions(manage_guild=True)
@app_commands.describe(
    canal="Canal donde se enviará el mensaje",
    texto="El texto que quieres que aparezca en el mensaje",
)
async def reglas(interaction: discord.Interaction, canal: discord.TextChannel, texto: str):
    gid = interaction.guild.id
    embed = discord.Embed(
        title="📋 『SERVER RULES』",
        description=texto,
        color=discord.Color.blurple(),
    )
    if interaction.guild.icon:
        embed.set_thumbnail(url=interaction.guild.icon.url)

    await canal.send(embed=embed)
    await interaction.response.send_message(t(gid, "reglas_ok", canal=canal.mention), ephemeral=True)


# ── /kick ────────────────────────────────────────────────────
@tree.command(name="kick", description="Expulsa a un usuario del servidor")
@app_commands.checks.has_permissions(kick_members=True)
@app_commands.describe(
    usuario="Usuario que quieres expulsar",
    razon="Motivo de la expulsión (opcional)",
)
async def kick(interaction: discord.Interaction, usuario: discord.Member, razon: str = "Sin razón especificada"):
    gid = interaction.guild.id

    try:
        await usuario.kick(reason=razon)
        await interaction.response.send_message(t(gid, "kick_ok", usuario=usuario, razon=razon))
    except discord.Forbidden:
        await interaction.response.send_message(t(gid, "kick_sin_permisos"), ephemeral=True)


# ── /xp ──────────────────────────────────────────────────────
@tree.command(name="xp", description="Da (o quita) XP a un usuario")
@app_commands.checks.has_permissions(manage_guild=True)
@app_commands.describe(
    usuario="Usuario al que le darás XP",
    cantidad="Cantidad de XP a otorgar (usa un número negativo para quitar)",
)
async def xp(interaction: discord.Interaction, usuario: discord.Member, cantidad: int):
    gid = interaction.guild.id
    data = cargar_xp()
    user_id = str(usuario.id)
    data[user_id] = max(0, data.get(user_id, 0) + cantidad)
    guardar_xp(data)

    signo = "+" if cantidad >= 0 else ""
    await interaction.response.send_message(
        t(gid, "xp_ok", usuario=usuario, total=data[user_id], signo=signo, cantidad=cantidad)
    )


# ── /rol ─────────────────────────────────────────────────────
@tree.command(name="rol", description="Le da un rol a un usuario")
@app_commands.checks.has_permissions(manage_roles=True)
@app_commands.describe(
    usuario="Usuario al que le darás el rol",
    rol="Rol que quieres asignar",
)
async def rol(interaction: discord.Interaction, usuario: discord.Member, rol: discord.Role):
    gid = interaction.guild.id

    if rol in usuario.roles:
        await interaction.response.send_message(t(gid, "rol_ya_tiene", usuario=usuario, rol=rol.name), ephemeral=True)
        return

    try:
        await usuario.add_roles(rol)
        await interaction.response.send_message(t(gid, "rol_ok", usuario=usuario, rol=rol.name))
    except discord.Forbidden:
        await interaction.response.send_message(t(gid, "rol_sin_permisos"), ephemeral=True)


# ── /nivel (consultar XP) ───────────────────────────────────
@tree.command(name="nivel", description="Muestra el XP de un usuario")
@app_commands.describe(usuario="Usuario a consultar (por defecto, tú mismo)")
async def nivel(interaction: discord.Interaction, usuario: discord.Member = None):
    gid = interaction.guild.id
    usuario = usuario or interaction.user
    data = cargar_xp()
    xp_actual = data.get(str(usuario.id), 0)
    await interaction.response.send_message(t(gid, "nivel_ok", usuario=usuario, xp=xp_actual))


# ── Manejo de errores de permisos (para todos los comandos) ─
@reglas.error
@kick.error
@xp.error
@rol.error
@apply.error
@idioma.error
async def comandos_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(t(interaction.guild.id, "sin_permiso"), ephemeral=True)
    else:
        raise error


if not DISCORD_TOKEN:
    raise RuntimeError(
        "❌ No se encontró DISCORD_TOKEN. Crea un archivo .env con la línea:\n"
        "DISCORD_TOKEN=tu_token_aqui"
    )

client.run(DISCORD_TOKEN)
