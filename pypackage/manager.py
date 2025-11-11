from pypackage.connection import con
import datetime as dt
import psycopg2
import logging

# TODO: replace print with loggers --done
# TODO: add try except to a decorator and reuse on every function there should be one or more general decorators that you should use. --done testing remains
# TODO: use proper type hinting with all the function --done
# TODO: use proper doc strings --done
# TODO: add precommits for formatting --done
# TODO: rename file to connection and manager , place them in a folder and create the package




# We can also use it directly without creating an object ,but when created with object we know which file's log is this


#Default logging level is warning, so to change it we have to 

logging.basicConfig(filename='logger.txt',level=logging.INFO)
logger = logging.getLogger(__name__)


def decor(func): 
        
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
    

    @decor
    def add_book(self,title : str, author : str, published_year : int, copies : int)-> None:
        '''   For adding the data inside the book  '''
        self.curr.execute("insert into library.books (title,author,published_year,available_copies) values(%s,%s,%s,%s)",(title,author,published_year,copies))
        self.curr.commit()
        logger.info("BOOK ADDED SUCCESSFULLY :)")


    @decor
    def get_book_by_id(self,book_id : int) -> None: 
        '''   Retrieve book details '''
        self.curr.execute("select * from library.books where book_id = %s",
                        (book_id,))
        data = self.curr.fetchall()
        logger.info(data)



    @decor
    def get_all_books(self):
        ''' LIST ALL BOOKS'''
        self.curr.execute("select book_id,title,author,published_year,available_copies from library.books")
        data = self.curr.fetchall()
        logger.info(data)

    
    


    @decor
    def update_book_copies(self,book_id : int, copies : int)-> None: 
        '''Update available copies'''
        self.curr.execute("update library.books set available_copies = %s where book_id = %s",(copies,book_id))
        self.curr.commit()            
        logger.info("UPDATE SUCCESSFULL !!")





    @decor
    def search_books(self,keyword : str) -> None: 
        '''Search books by title or author'''
        keyword = f"%{keyword}%"
        self.curr.execute("select * from library.books where title ilike %s or author ilike %s",(keyword,keyword) )
        data = self.curr.fetchall()
        logger.info(data)



    @decor
    def add_member(self,name : str, email : str, phone : int) -> None: 
        ''' Register a new member'''
        self.curr.execute("insert into library.members (name,email,phone) values(%s,%s,%s)",(name,email,phone) )
        self.curr.commit()
        logger.info("DATA INSERTED SUCCESSFULLY!!")




    @decor
    def get_member_by_id(self,member_id : int) -> None: 
        '''Retrieve member details'''
        self.curr.execute("select * from library.members where member_id = %s",(member_id,) )
        logger.info(self.curr.fetchall())




    @decor
    def get_all_members(self) -> None: 
        '''List all members'''
        self.curr.execute("select * from library.members" )
        logger.info(self.curr.fetchall())







    @decor
    def borrow_book(self,book_id : int, member_id : int, days : int = 14)-> None: 
        '''Create a loan record'''
        date = dt.date.today() + dt.timedelta(days=days)
        self.curr.execute("insert into library.loans (book_id,member_id,due_date,status) values (%s,%s,%s,%s)",(book_id,member_id,date,"active") )
        self.curr.commit()            
        logger.info("DATA INSERTED IN LOANS TABLE!!!")


    @decor
    def return_book(self,loan_id : int) ->None: 
        '''Mark book as returned'''
        self.curr.execute("update library.loans set status = 'returned' where loan_id = %s",(loan_id,) )
        logger.info("UPDATED LOANS TABLE!!!")
        self.curr.commit()




    @decor
    def get_active_loans(self) ->None: 
        ''' List all active loans'''
        self.curr.execute("select * from library.loans where status = 'active' " )
        logger.info(self.curr.fetchall())


    @decor
    def get_overdue_loans(self) -> None: 
        '''List overdue loans'''
        date = dt.date.today()
        self.curr.execute("select * from library.loans where due_date < %s ",(date,) )
        logger.info(self.curr.fetchall())



    @decor
    def get_most_borrowed_books(self,limit : int = 5 ) -> None:
        '''Return top borrowed books'''
        self.curr.execute(''' 
            select lb.book_id,title,author,published_year from
            library.books as lb inner join (select book_id from
            library.loans group by book_id order by 
            count(book_id) desc limit %s) as bk on lb.book_id = bk.book_id''',
            (limit,) )
        
        logger.info(self.curr.fetchall())
            


    @decor
    def get_member_history(self,member_id : int) -> None:
        '''Get complete borrowing history for a member'''
        self.curr.execute("select * from library.loans where member_id = %s",(member_id,) )
        logger.info(self.curr.fetchall())
            
     

    @decor
    def get_books_never_borrowed(self) -> None:
        '''List books that have never been borrowed'''
        self.curr.execute('''select tb1.book_id,title,author,published_year from 
                    library.books as tb1 where tb1.book_id not in 
                    (select book_id from library.loans group by book_id)''')
        
        logger.info(self.curr.fetchall())
       
    @decor
    def get_statistics(self) -> dict[str , int | str | None]:
        '''Return a dictionary with:'''
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

      


'''
Total books
Total members
Active loans
Overdue loans
Most active member
'''











    