from tkinter import *
from tkinter import ttk



# def fn_sort_column(treeview: ttk.Treeview, col, reverse: bool):
#   """ Trier le treeview en cliquant sur les entêtes de colonne """
#   try:
#       data_list = [(int(treeview.set(k,col)), k) for k in treeview.get_children("")]
#   except Exception:
#       data_list = [(treeview.set(k,col), k) for k in treeview.get_children("")]

#   data_list.sort(reverse=reverse)


#   for index, (val, k) in enumerate(data_list):
#       treeview.move(k, "", index)

#   treeview.heading(column=col,text=col,command=lambda _col=col: fn_sort_column(treeview, _col, not reverse))




from functools import partial


class MyTreeview(ttk.Treeview):
	def heading(self, column, sort_by=None, **kwargs):
		if sort_by:
			func = getattr(self, f"_sort_by_{sort_by}", None)
			if func:
				kwargs['command'] = partial(func, column, False)
		return super().heading(column, **kwargs)




	def _sort(self, column, reverse, data_type, callback):
		l = [(self.set(k, column), k) for k in self.get_children('')]
		l.sort(key=lambda t: data_type(t[0]), reverse=reverse)
		for index, (_, k) in enumerate(l):
			self.move(k, '', index)
		self.heading(column, command=partial(callback, column, not reverse))

	def _sort_by_num(self, column, reverse):
		self._sort(column, reverse, int, self._sort_by_num)
		# if reverse:
		#   self.heading('number', text='number \\', sort_by='num')
		# else:
		#   self.heading('number', text='number /', sort_by='num')

	def _sort_by_name(self, column, reverse):
		self._sort(column, reverse, str, self._sort_by_name)

	def _sort_by_date(self, column, reverse):
		def _str_to_datetime(string):
			return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
		self._sort(column, reverse, _str_to_datetime, self._sort_by_date)

...
# Some code
...


def fn_sort(column):
	# Lister les éléments de la colonne
	l = [(treeview.set(k, column), k) for k in treeview.get_children('')]
	# Récupération du dictionnaire de la valeur de tri
	reverse = dict_sort.setdefault(column, False)
	# Trier les éléments de la colonne
	l.sort(key=lambda t: t[0], reverse=reverse)
	for index, (_, k) in enumerate(l):
		treeview.move(k, '', index)
	dict_sort[column] = not reverse
	if reverse:
		treeview.heading(column='number', text="number \\")
	else:
		treeview.heading(column='number', text="number /")




win_main = Tk()
treeview = ttk.Treeview(win_main, columns=("number", "name", "date"))


treeview.heading(column='number', text="number", command=lambda: fn_sort("number"))
treeview.heading(column='name', text='name', command=lambda: fn_sort("name"))
treeview.heading(column='date', text='date')
treeview.insert('', 'end', iid=5, values=("test2", "2", "2021-09-10"))
treeview.insert('', 'end', iid=1, values=("test1", "1", "2021-09-09"))

dict_sort = {} 



treeview.pack()

win_main.mainloop()























# if __name__ == "__main__":
#   fn_sort_column()