import discord
from discord.ext import commands

class CustomHelpCommand(commands.HelpCommand):
    color = 0x8080ff
    def footer(self):
        return f"{self.clean_prefix}{self.invoked_with} <command> for more details"

    def get_command_signature(self, command):
        return f"```yaml\n{self.clean_prefix}{command.qualified_name} {command.signature}```"
      
    async def send_command_help(self, command):
        #em = discord.Embed(title=command.qualified_name, color=self.color)
        em = discord.Embed(title=command.qualified_name, color=self.color)
        if command.help:
            em.description = command.help
        elif command.brief:
            em.description = command.brief
        
        em.add_field(name="Syntax", value=self.get_command_signature(command))
        #em.set_footer(text=self.footer())
        await self.get_destination().send(embed=em)

    async def send_bot_help(self, mapping):
        em = discord.Embed(title="Help", description="Hey, I\'m Dio or you can call me Di!", color=self.color)
        for cog, commands in mapping.items():
            #if not cog:
            #    continue

            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                value = "\t".join(f"`{i.name}` `{i.brief if i.brief != None else i.help}`\n" for i in commands)
                em.add_field(name="Commands", value=value)
        em.set_footer(text=self.footer())
        await self.get_destination().send(embed=em)
