var Discord = require('discord.io');
var logger = require('winston');
var auth = require('./auth.json');
var helpQueue = new Array();
// Configure logger settings
logger.remove(logger.transports.Console);
logger.add(new logger.transports.Console, {
    colorize: true
});
logger.level = 'debug';
var bot = new Discord.Client({
   token: auth.token,
   autorun: true
});
bot.on('ready', function (evt) {
});
bot.on('message', function (user, userID, channelID, message, evt) {
    if (message.substring(0, 1) == '!') {
        var cmd = message.substring(1).split(' ')[0];

        switch(cmd) {
            case 'please_help_mr_reyes':
                helpQueue.push(userID);
            break;
         }
     }
});
