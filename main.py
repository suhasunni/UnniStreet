from Reddit import Stock
import tkinter as tk  
from tkinter import ttk

#Tkinter graphics
class Screen:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Welcome to Unni Street')
        self.window.geometry('500x300')
        
        #UNNI STREET title
        self.unni_street_lb = tk.Label(self.window,text='Unni Street',font=('Times',35,'bold'))
        self.unni_street_lb.place(x=250,y=40,anchor='center')
        
        #Text under title
        self.description_lb = tk.Label(self.window,text='An M.L. project by Suhas Unni',font=('Times',15,'italic'))
        self.description_lb.place(x=250,y=75,anchor='center')
        
        #Face images 
        self.face_img1 = tk.PhotoImage(file='face.png')
        self.face_img1_lb = tk.Label(self.window, image=self.face_img1)
        self.face_img1_lb.place(x=75,y=40,anchor='center')
        self.face_img2 = tk.PhotoImage(file='reversedface.png')
        self.face_img2_lb = tk.Label(self.window,image=self.face_img2)
        self.face_img2_lb.place(x=425,y=40,anchor='center')
        
        #Question label
        self.stock_check_lb = tk.Label(self.window,text='What Stock Would You Like to Check? (e.g NVDA, AAPL, AMZN)',font=('Times',12))
        self.stock_check_lb.place(x=250,y=150,anchor='center')
        
        #Textbox
        self.textbox = tk.Entry(self.window)
        self.textbox.place(x=250,y=175,anchor='center')
        
        #Get prediction button
        self.predict_b = tk.Button(self.window,text='Get Reccomendation',command=lambda:self.get_reccomendation(self.textbox.get()))
        self.predict_b.place(x=130,y=210,anchor='center')
        
        #View posts button
        self.view_posts_b = tk.Button(self.window,text='View Posts',command=lambda:self.view_posts(self.textbox.get()))
        self.view_posts_b.place(x=240,y=210,anchor='center')
        
        #About the model button
        self.about_the_model_lb = tk.Button(self.window,text='About the Model',command=lambda:self.about_the_model())
        self.about_the_model_lb.place(x=340,y=210,anchor='center')
    
        #Reccomendations label
        self.reccomendation_lb = tk.Label(self.window,text='')
        self.reccomendation_lb.place(x=250,y=250,anchor='center')
        
        #Quit button
        self.quit_b = tk.Button(self.window,text='Quit',command=lambda:self.window.destroy())
        self.quit_b.place(x=240,y=280,anchor='center')
        
        self.window.mainloop()
    
    #Display simple text reccomendation
    def get_reccomendation(self,stock_name):
        #Create instance of reddit API/sentiment analysis
        user_stock = Stock(stock_name)
        #Obtain over sentiment score of stock (average of each induvidual post score)
        sentiment_score = user_stock.get_overall_score(user_stock.get_scores())   
        
        #Display reccomendatin message based on sentiment score 
        if not sentiment_score:
            reccomendation = 'hmm...it looks like no one is talking about your stock...\nyou might know something that we don\'t!'
        
        elif sentiment_score[0] == 0: 
            reccomendation = f'{stock_name} has a neutral sentiment, so no strong opinions either way. \nKeep an eye on it for any changes.'
        
        elif sentiment_score[0] > 0 and sentiment_score[0] < 100:
            reccomendation = f'{stock_name} has a slightly positive sentiment, investing would be a good idea!'
        
        elif sentiment_score[0] > 100:
            reccomendation = f'Buy, buy, buy! {stock_name} has an extremly high sentiment!'
        
        elif sentiment_score[0] < 0:
            reccomendation = f'Oh no! Looks like you should stay away from {stock_name} right now!\nMayhaps consider puts!'
        
        #Display reccomendation
        self.reccomendation_lb.config(text=reccomendation)   

    #Display all posts mentioning stock and associated sentiment
    def view_posts(self,stock_name): 
        #Create new window
        view_window = tk.Tk()
        view_window.geometry('500x700')
        view_window.title('View') 
        
        #SCROLL WHEEL
        main_frame = tk.Frame(view_window)
        main_frame.pack(fill='both',expand=1)
        
        #Create a new canvas
        my_canvas = tk.Canvas(main_frame)
        my_canvas.pack(side='left',fill='both',expand=1)
        
        #Create instance of a scroll wheel
        scrollbar = ttk.Scrollbar(main_frame,orient='vertical',command=my_canvas.yview)
        scrollbar.pack(side='right',fill='y')
        
        #Configure scroll wheel
        my_canvas.configure(yscrollcommand=scrollbar.set)
        my_canvas.bind('<Configure>',lambda e:my_canvas.configure(scrollregion=my_canvas.bbox('all')))
        
        #Create left frame
        other_frame = tk.Frame(my_canvas)
        my_canvas.create_window((0,0),window=other_frame,anchor='nw')
        
        #'Posts Mentioning Stock Name' label
        title = tk.Label(other_frame,text=f'Posts Mentioning {stock_name}',font=('Times',15,'bold'))
        title.grid(row=0,column=0,padx=5,pady=5)
        
        #'Sentiment Score' label
        title_2 = tk.Label(other_frame,text='Sentiment Score',font=('Times',15,'bold'))
        title_2.grid(row=0,column=1,padx=5,pady=5)
        
        #Create instance of Reddit API/Sentiment analysis
        user_stock = Stock(stock_name)
        
        #Get list of sentiment scores
        list_of_scores = user_stock.get_scores()
        #Get list of post titles
        list_of_titles = user_stock.get_titles()
               
        #Sort lists in decending order of sentiment
        for i in range(len(list_of_scores)):
            max = i
            for j in range(i+1,len(list_of_scores)):
                if list_of_scores[j]>list_of_scores[max]:
                    max = j
            list_of_scores[i],list_of_scores[max]=list_of_scores[max],list_of_scores[i]
            list_of_titles[i],list_of_titles[max]=list_of_titles[max],list_of_titles[i]
        
        #Display each post title with associated sentiment score in row/column format
        for i in range(len(list_of_titles)):
            #Create label for post
            post_lb = tk.Label(other_frame,text=list_of_titles[i])
            post_lb.grid(row=i+1,column=0,padx=5,pady=5)
            
            #Create label for sentiment score
            sentiment_lb = tk.Label(other_frame,text=list_of_scores[i])
            sentiment_lb.grid(row=i+1,column=1,padx=5,pady=5)

        view_window.mainloop()

    #Small paragraph about the model
    def about_the_model(self):
        about_window = tk.Tk()
        about_window.geometry('600x300')
        about_window.title('About the Model')
        
        title_lb = tk.Label(about_window,text='About',font=('Times',15,'bold'))
        title_lb.pack()
        
        description = ''' 
        'Unni Street' is a unique stock reccomendation platform powered by the collective insights\n
        of the largest trading forum in the world: r/wallstreetbets. Developed in Python, the model\n
        uses sentiment analysis to interpret the latest trends and sentiments expressed in posts\n
        on the forum. Utilising a custom-built model fine-tuned for unique slang and vocabulary,\n
        the application sifts through the noise to generate actionable stock reccomendations.\n
        Stay ahead of the market with Unni Street's indights, based on the latest buzz from the\n
        world's most influential online trading forums.
        '''
        
        text_lb = tk.Label(about_window,text=description,font=('Times',10))
        text_lb.pack()
        
#Create instance of program
screen = Screen()   