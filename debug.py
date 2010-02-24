try:
    from IPython.Shell import IPShellEmbed
    ipython = IPShellEmbed()
    import ipdb
    idebug = ipdb.set_trace
except:
    def nothing():
        pass
    ipython = nothing
    idebug = nothing
    