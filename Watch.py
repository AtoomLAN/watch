import fcntl, os, struct, sys, termios, time
import BasicCli, CliParser, Tac

class Watch( object ):
    DEFAULT_INTERVAL = 2.0
    DRAGON = """
                    __        _
                  _/  \    _(\(o
                 /     \  /  _  ^^^o
                /   !   \/  ! '!!!v'
               !  !  \ _' ( \____
               ! . \ _!\   \===^\)      Here be dragons
                \ \_!  / __!
                 \!   /    \\
           (\_      _/   _\ )
            \ ^^--^^ __-^ /(__
             ^^----^^    "^--v'
    """

    def __call__( self, mode, command, interval ):
        interval = float( interval )
        if interval < 0.1:
            interval = 0.1

        while not Tac.checkInterrupt():
            print "\x1b[2J\x1b[H%s\n" % self._format_title( command, interval )
            if command == "dragons":
                print Watch.DRAGON
            else:
                mode.session.runCmd( command )
            sys.stdout.flush()
            time.sleep( interval )   
 
    def _format_title( self, command, interval ):
        screen_width = BasicCli.ioctl_GWINSZ()[1]
        if screen_width == 0:
            screen_width = 80

        title = "Every %.1fs: %s" % ( interval, command )
        title_time = time.strftime( "%a %b %d %H:%M:%S %Y" )
        title_size = screen_width - len(title) - len(title_time)

        if len(title) > title_size:
            title = title[:title_size - 4] + "... " + title_time
        else:
            title = title + " " * title_size + title_time

        return title

tokenWatch = CliParser.KeywordRule( "watch",
                                    "Execute a command periodically" )

watchCommandRule = CliParser.StringRule( name="command",
                                         helpname="command",
                                         helpdesc="Executable command" )

watchFloatRule = CliParser.PatternRule( "\d*\.?\d+",
                                         name="interval",
                                         helpname="interval",
                                         helpdesc="Interval to run the command at" )

watchIntervalRule = CliParser.OptionalRule( watchFloatRule,
                                            Watch.DEFAULT_INTERVAL,
                                            name="interval" )

BasicCli.UnprivMode.addCommand ( ( tokenWatch,
                                   watchIntervalRule, watchCommandRule,
                                   Watch() ), )

BasicCli.EnableMode.addCommand ( ( tokenWatch,
                                   watchIntervalRule, watchCommandRule,
                                   Watch() ), )
