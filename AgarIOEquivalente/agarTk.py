#!/usr/bin/env python

import Tk

class VentanaAgar(Tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.frame = tk.Frame.__init__(self, parent, estadoDeJuego, *args, **kwargs)
        self.parent = parent

        canvas = tk.Canvas(self.frame, width=600, height=200)
        canvas.pack()

        self.estadoDeJuego = estadoDeJuego

        self.boton = tk.Button(self.frame, text="Iniciar juego")
        self.boton.pack()
        
        self.updateEstado() #Utilizar la cola para seguir

    def updateEstado():
        if not self.estadoDeJuego.empty():
            item = self.estadoDeJuego.get()
            
        
        

if __name__=="__main__":
    print 'Beginning Tkinter'
    
    root = tk.Tk()
    VentanaAgar(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
