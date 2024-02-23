from src.interface import Interface

def main():
    # Start application
    app = Interface()
    app.set_background_image('img/stars.jpg')
    app.set_title("Automated Gene Annotation Table Interface") 
    app.window.mainloop()

if __name__ == "__main__":
    main()



