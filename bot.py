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
idioma_servidor = {}

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
    },
}


def t(guild_id, clave, **kwargs):
    lang = idioma_servidor.get(guild_id, "es")
    texto = TEXTOS[lang].get(clave, TEXTOS["es"].get(clave, clave))
    return texto.format(**kwargs) if kwargs else texto


@client.event
async def on_ready():
    if GUILD_ID:
        guild = discord.Object(id=GUILD_ID)
        tree.copy_global_to(guild=guild)
        await tree.sync(guild=guild)  # instantáneo, solo en ese servidor
    else:
        await tree.sync()  # global, puede tardar hasta 1 hora en aparecer

    print(f"✅ Bot conectado como: {client.user}")


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
