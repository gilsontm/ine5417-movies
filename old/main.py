from tkinter import *
from tkinter.ttk import *
from utils import apis
from utils import image_tools

class Main(Frame):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.images = []
        self.tmdb_api = apis.get_tmdb_api()
        self.create_gui()
        mouse_wheel = lambda e: self.canvas.yview_scroll(1 if e.num == 5 else -1, "units")
        self.root.bind("<Button-4>", mouse_wheel)
        self.root.bind("<Button-5>", mouse_wheel)

    def create_gui(self):
        self.master.title("Movies & TV")
        self.pack(fill=BOTH, expand=True)
        self.style = Style()
        self.style.theme_use("clam")

        """ VERTICAL SCROLLBAR """
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        """ HEADER """
        header = Frame(self, relief=RAISED, padding=10, height=10)
        header.pack(side=TOP)

        self.search_input = Entry(header)
        self.search_input.pack(side=TOP)
        self.search_input.grid(row=0, column=0, padx=5, ipadx=100, ipady=5)

        button = Button(header, text="Pesquisar", command=self.search)
        button.grid(row=0, column=1, padx=5)

        """ BODY """
        self.body = Frame(self, borderwidth=2)
        self.body.pack(fill=BOTH, expand=True, side=TOP)

        self.canvas = Canvas(self.body, width=800, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.canvas.yview)

        self.image_container = Frame(self.canvas, width=800)
        self.canvas.pack(side=TOP, expand=True, fill=Y)
        self.canvas.create_window((400, 0), window=self.image_container, anchor=N)
        self.update_canvas()

    def search(self):
        self.delete_images()

        query = self.search_input.get()
        if query:
            search = self.tmdb_api.Search()
            promise = search.multi(query=query)
            for result in search.results:
                if result["media_type"] == "movie":
                    path = result["poster_path"]
                    name = result["title"]
                if result["media_type"] == "tv":
                    path = result["poster_path"]
                    name = result["original_name"]
                if result["media_type"] == "person":
                    path = result["profile_path"]
                    name = result["name"]
                photo = image_tools.get_image_or_default(path)
                row = 2 * (len(self.images) // 4); column = len(self.images) % 4
                self.images.append(photo)
                poster = Label(self.image_container, image=photo)
                poster.grid(row=row, column=column, padx=0, pady=10)
                title = Label(self.image_container, text=name, wraplength=185, justify=CENTER)
                title.grid(row=row+1, column=column)
        if len(self.images) == 0:
            label = Label(self.image_container, text="Nenhum resultado encontrado.", justify=CENTER)
            label.pack(side=TOP)

        self.update_canvas()

    def update_canvas(self):
        self.body.update()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def delete_images(self):
        for child in self.image_container.winfo_children():
            child.destroy()
        self.images = []

if __name__ == "__main__":
    root = Tk()
    root.geometry("900x600")
    frame = Main(root)
    root.mainloop()