from pypackage.connection import con
import datetime as dt
import psycopg2
import logging



# TODO: create pull requests --done
# TODO: rename the decorator function and use doc strings properly --done
# TODO: configure the pre commit file properly and push it on github --done
# TODO: Name the commits properly --donoe
# TODO: use the multi line string --done



logging.basicConfig(filename='logger.txt',level=logging.INFO)
logger = logging.getLogger(__name__)


def Decorator(func): 
    '''This decorator will perform the try except block for all functions instead of individual try except block in each function '''
        
    def wrapper(self, *args, **kwargs):
        try:
            self.curr = self.con.cursor()
            
            return func(self, *args, **kwargs)

        except psycopg2.Error as err:

            self.curr.rollback()
            logger.setLevel(logging.ERROR)
            print("ERROR:",err)
            logger.error(f"ERROR!!: {err}")
            logger.setLevel(logging.INFO)

        finally:
            self.curr.close()

    return wrapper





class managment:


    def __init__(self):

            self.con = con.connect()
    

    @Decorator
    def add_book(self,title : str, author : str, published_year : int, copies : int)-> None:
        '''   This function adds data inside the book table in schema library '''
        self.curr.execute("insert into library.books (title,author,published_year,available_copies) values(%s,%s,%s,%s)",(title,author,published_year,copies))
        self.curr.commit()
        logger.info("BOOK ADDED SUCCESSFULLY :)")


    @Decorator
    def get_book_by_id(self,book_id : int) -> None: 
        '''  This function Retrieve book details using the book id'''
        self.curr.execute("select * from library.books where book_id = %s",
                        (book_id,))
        data = self.curr.fetchall()
        logger.info(data)



    @Decorator
    def get_all_books(self):
        ''' This function reterive all records from the books table'''
        self.curr.execute("select book_id,title,author,published_year,available_copies from library.books")
        data = self.curr.fetchall()
        logger.info(data)

    
    


    @Decorator
    def update_book_copies(self,book_id : int, copies : int)-> None: 
        ''' this function updates the available copies of a book using its book id '''
        self.curr.execute("update library.books set available_copies = %s where book_id = %s",(copies,book_id))
        self.curr.commit()            
        logger.info("UPDATE SUCCESSFULL !!")





    @Decorator
    def search_books(self,keyword : str) -> None: 
        '''this function searches books by it title or author '''
        keyword = f"%{keyword}%"
        self.curr.execute("select * from library.books where title ilike %s or author ilike %s",(keyword,keyword) )
        data = self.curr.fetchall()
        logger.info(data)



    @Decorator
    def add_member(self,name : str, email : str, phone : int) -> None: 
        '''this function register a new member in members table in schema library'''
        self.curr.execute("insert into library.members (name,email,phone) values(%s,%s,%s)",(name,email,phone) )
        self.curr.commit()
        logger.info("DATA INSERTED SUCCESSFULLY!!")




    @Decorator
    def get_member_by_id(self,member_id : int) -> None: 
        ''' this function retrieves member details using the member id '''
        self.curr.execute("select * from library.members where member_id = %s",(member_id,) )
        logger.info(self.curr.fetchall())




    @Decorator
    def get_all_members(self) -> None: 
        '''this function list all members in the members table '''
        self.curr.execute("select * from library.members" )
        logger.info(self.curr.fetchall())







    @Decorator
    def borrow_book(self,book_id : int, member_id : int, days : int = 14)-> None: 
        ''' this function creates a loan record for individual member in loans table in schema library '''
        date = dt.date.today() + dt.timedelta(days=days)
        self.curr.execute("insert into library.loans (book_id,member_id,due_date,status) values (%s,%s,%s,%s)",(book_id,member_id,date,"active") )
        self.curr.commit()            
        logger.info("DATA INSERTED IN LOANS TABLE!!!")


    @Decorator
    def return_book(self,loan_id : int) ->None: 
        ''' this function marks book as returned using the loan id '''
        self.curr.execute("update library.loans set status = 'returned' where loan_id = %s",(loan_id,) )
        logger.info("UPDATED LOANS TABLE!!!")
        self.curr.commit()




    @Decorator
    def get_active_loans(self) ->None: 
        '''  this function lists all active loans '''
        self.curr.execute("select * from library.loans where status = 'active' " )
        logger.info(self.curr.fetchall())


    @Decorator
    def get_overdue_loans(self) -> None: 
        '''this function list overdue loans '''
        date = dt.date.today()
        self.curr.execute("select * from library.loans where due_date < %s ",(date,) )
        logger.info(self.curr.fetchall())



    @Decorator
    def get_most_borrowed_books(self,limit : int = 5 ) -> None:
        '''this function shows top borrowed books from loans '''
        self.curr.execute(''' 
            select lb.book_id,title,author,published_year from
            library.books as lb inner join (select book_id from
            library.loans group by book_id order by 
            count(book_id) desc limit %s) as bk on lb.book_id = bk.book_id''',
            (limit,) )
        
        logger.info(self.curr.fetchall())
            


    @Decorator
    def get_member_history(self,member_id : int) -> None:
        '''this function shows complete borrowing history for a member using the member id '''
        self.curr.execute("select * from library.loans where member_id = %s",(member_id,) )
        logger.info(self.curr.fetchall())
            
     

    @Decorator
    def get_books_never_borrowed(self) -> None:
        '''tbis function list books that have never been borrowed '''
        self.curr.execute('''select tb1.book_id,title,author,published_year from 
                    library.books as tb1 where tb1.book_id not in 
                    (select book_id from library.loans group by book_id)''')
        
        logger.info(self.curr.fetchall())


       
    @Decorator
    def get_statistics(self) -> dict[str , int | str | None]:
        ''' Return a dictionary with: Total books, Total members ,Active loans ,Overdue loans Most active member '''
        self.curr.execute('''with cte as (
    select count(*) as count, member_id
    from library.loans
    group by member_id
),
cte2 as (
    select status, count(status) as count
    from library.loans
    group by status
)
select 
    (select count(book_id) from library.books) as total_books,
    (select count(member_id) from library.members) as total_members,
    (select count from cte2 where status = 'active') as active_loans,
    (select member_id from cte where count = (select max(count) from cte) limit 1) as most_active_member;
''')
            
        result = self.curr.fetchall()    
        dict1 = {
            'Total books':result[0][0],
            'total members':result[0][1],
            'active loans':result[0][2],
            'most active member"s id':result[0][3]
        }
        print(dict1)
        return dict1

        

    def __del__(self) -> None:
        con.disconnect(self.con)

      










    