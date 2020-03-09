Dev environment preparation

1.pipenv shell (get into virtual environment, you must have pipenv installed on your local system)
2.pipenv install (install all dependency)

Q:How to fix  pip install mysqlclient ERROR on Macbookpro?
A:Follow this link for detail
https://medium.com/@shandou/pipenv-install-mysqlclient-on-macosx-7c253b0112f2



Git:
1. (any):git checkout master (switch to master)
2. (master):git pull (update from github)
3. (master):git checkout -b xxx (switch to your own branch)
4. (xxx):git merge master (update your own branch from master)
	loop:
		do some dev on your own branch
		(xxx):git add ...
		(xxx):git commit ...
		(xxx):git push(not necessary, if you don't want to merge to master by now, you can push to your own branch on github)
5. (xxx):git checkout master 
6. (master):git merge xxx (merge your branch to master)
7. (master):git push (push to github)