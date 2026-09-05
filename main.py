import discord
import asyncio
import getpass
import subprocess

AZUL = "\033[94m"
RESET = "\033[0m"

MAX_CANAIS = 10
MAX_MSG_POR_CANAL = 2
MAX_ENVIO = 1
MAX_BANS = 2


def titulo():
    resultado = subprocess.run(
        ["figlet", "HACK DISCORD"],
        capture_output=True,
        text=True
    )

    print(AZUL + resultado.stdout + RESET)


def linha():
    print(AZUL + "================================================" + RESET)


def caixa():
    print(AZUL + "+----------------------------------------------+" + RESET)
    print(
        AZUL +
        "| Painel feito por high use o painel a vontade <3 |"
        + RESET
    )
    print(AZUL + "+----------------------------------------------+" + RESET)


async def painel(bot, guild):

    while True:
        print()

        linha()
        titulo()
        caixa()
        linha()

        print(AZUL + f"Servidor: {guild.name}" + RESET)
        print(AZUL + f"ID: {guild.id}" + RESET)

        linha()

        print(AZUL + "[1] Criar canais" + RESET)
        print(AZUL + "[2] Mandar mensagens" + RESET)
        print(AZUL + "[3] Informacoes do servidor" + RESET)
        print(AZUL + "[4] Banir membros" + RESET)
        print(AZUL + "[5] Sair" + RESET)

        linha()

        opcao = input(
            AZUL + "Escolha uma opcao: " + RESET
        ).strip()

        if opcao == "1":

            nome = input(
                AZUL + "Nome dos canais: " + RESET
            ).strip()

            if not nome:
                print(AZUL + "Nome invalido." + RESET)
                continue

            try:
                quantidade = int(
                    input(
                        AZUL +
                        "Quantidade de canais (maximo 10): " +
                        RESET
                    )
                )
            except ValueError:
                print(AZUL + "Digite um numero valido." + RESET)
                continue

            if quantidade < 1 or quantidade > MAX_CANAIS:
                print(AZUL + "O limite e 10 canais." + RESET)
                continue

            try:
                mensagens = int(
                    input(
                        AZUL +
                        "Mensagens em cada canal (maximo 2): " +
                        RESET
                    )
                )
            except ValueError:
                print(AZUL + "Digite um numero valido." + RESET)
                continue

            if mensagens < 1 or mensagens > MAX_MSG_POR_CANAL:
                print(AZUL + "O limite e 2 mensagens." + RESET)
                continue

            texto = input(
                AZUL + "Mensagem: " + RESET
            ).strip()

            if not texto:
                print(AZUL + "Mensagem vazia." + RESET)
                continue

            criados = 0

            for _ in range(quantidade):

                try:
                    canal = await guild.create_text_channel(
                        name=nome
                    )

                    criados += 1

                    print(
                        AZUL +
                        f"[+] Canal criado: #{canal.name}" +
                        RESET
                    )

                    for _ in range(mensagens):
                        await canal.send(texto)

                    await asyncio.sleep(1)

                except discord.Forbidden:
                    print(
                        AZUL +
                        "O bot nao possui permissao para criar canais."
                        + RESET
                    )
                    break

                except discord.HTTPException as erro:
                    print(
                        AZUL +
                        f"Erro do Discord: {erro}" +
                        RESET
                    )
                    break

            print(
                AZUL +
                f"Canais criados: {criados}" +
                RESET
            )

        elif opcao == "2":

            texto = input(
                AZUL + "Mensagem: " + RESET
            ).strip()

            if not texto:
                print(AZUL + "Mensagem vazia." + RESET)
                continue

            try:
                quantidade = int(
                    input(
                        AZUL +
                        "Quantas vezes enviar (maximo 1): " +
                        RESET
                    )
                )
            except ValueError:
                print(AZUL + "Digite um numero valido." + RESET)
                continue

            if quantidade != 1:
                print(AZUL + "O limite e 1 envio." + RESET)
                continue

            canais = guild.text_channels

            for i, canal in enumerate(canais, 1):
                print(
                    AZUL +
                    f"[{i}] #{canal.name}" +
                    RESET
                )

            try:
                escolha = int(
                    input(
                        AZUL + "Escolha o canal: " + RESET
                    )
                )

                canal = canais[escolha - 1]

            except (ValueError, IndexError):
                print(AZUL + "Canal invalido." + RESET)
                continue

            try:
                await canal.send(texto)

                print(
                    AZUL +
                    "Mensagem enviada com sucesso." +
                    RESET
                )

            except discord.Forbidden:
                print(
                    AZUL +
                    "O bot nao pode enviar mensagens nesse canal." +
                    RESET
                )

        elif opcao == "3":

            linha()

            print(AZUL + "     INFORMACOES DO SERVIDOR" + RESET)

            linha()

            print(AZUL + f"Nome: {guild.name}" + RESET)
            print(AZUL + f"ID: {guild.id}" + RESET)
            print(AZUL + f"Membros: {guild.member_count}" + RESET)
            print(AZUL + f"Canais: {len(guild.channels)}" + RESET)

            linha()

        elif opcao == "4":

            print()
            print(AZUL + "BANIR MEMBROS" + RESET)
            print(AZUL + "Limite: 2 membros por execucao." + RESET)
            print()

            if not guild.me.guild_permissions.ban_members:
                print(
                    AZUL +
                    "O bot nao possui a permissao Ban Members."
                    + RESET
                )
                continue

            try:
                quantidade = int(
                    input(
                        AZUL +
                        "Quantos membros banir (1-2): " +
                        RESET
                    )
                )
            except ValueError:
                print(AZUL + "Numero invalido." + RESET)
                continue

            if quantidade < 1 or quantidade > MAX_BANS:
                print(AZUL + "O limite e 2 membros." + RESET)
                continue

            for i in range(quantidade):

                try:
                    membro_id = int(
                        input(
                            AZUL +
                            f"ID do membro {i + 1}: " +
                            RESET
                        )
                    )
                except ValueError:
                    print(AZUL + "ID invalido." + RESET)
                    continue

                membro = guild.get_member(membro_id)

                if membro is None:
                    print(AZUL + "Membro nao encontrado." + RESET)
                    continue

                if membro == guild.owner:
                    print(
                        AZUL +
                        "O dono do servidor nao pode ser banido."
                        + RESET
                    )
                    continue

                if membro == bot.user:
                    print(
                        AZUL +
                        "O bot nao pode banir a si mesmo."
                        + RESET
                    )
                    continue

                if membro.top_role >= guild.me.top_role:
                    print(
                        AZUL +
                        "O bot nao pode banir esse membro por causa "
                        "da hierarquia de cargos."
                        + RESET
                    )
                    continue

                try:
                    await guild.ban(
                        membro,
                        reason="Banido pelo painel"
                    )

                    print(
                        AZUL +
                        f"[+] {membro} foi banido."
                        + RESET
                    )

                except discord.Forbidden:
                    print(
                        AZUL +
                        "Discord recusou o banimento."
                        + RESET
                    )

                except discord.HTTPException as erro:
                    print(
                        AZUL +
                        f"Erro: {erro}" +
                        RESET
                    )

        elif opcao == "5":

            print(AZUL + "Saindo..." + RESET)

            await bot.close()
            return

        else:

            print(AZUL + "Opcao invalida." + RESET)


class PainelBot(discord.Client):

    def __init__(self):

        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True

        super().__init__(intents=intents)

    async def on_ready(self):

        print()

        titulo()
        caixa()

        print(
            AZUL +
            f"Bot conectado: {self.user}" +
            RESET
        )

        print()

        try:
            servidor_id = int(
                input(
                    AZUL +
                    "Digite o ID do servidor: " +
                    RESET
                )
            )
        except ValueError:
            print(AZUL + "ID invalido." + RESET)
            await self.close()
            return

        guild = self.get_guild(servidor_id)

        if guild is None:

            print(
                AZUL +
                "Servidor nao encontrado." +
                RESET
            )

            await self.close()
            return

        print(
            AZUL +
            f"Servidor encontrado: {guild.name}" +
            RESET
        )

        await painel(self, guild)


print()

titulo()
caixa()

print(
    AZUL +
    "Use o token do seu proprio bot." +
    RESET
)

print()

TOKEN = getpass.getpass(
    AZUL +
    "Token do bot: " +
    RESET
)

bot = PainelBot()

try:
    bot.run(TOKEN)

except discord.LoginFailure:

    print(
        AZUL +
        "Token invalido." +
        RESET
    )

except Exception as erro:

    print(
        AZUL +
        f"Erro: {erro}" +
        RESET
    )