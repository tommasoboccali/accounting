#scp tboccali@login.marconi.cineca.it:/marconi_work/Pra18_4658/accounting/accounting-saldo.out .
scp boccali@bastion.cnaf.infn.it:/data/CMS/boccali/Cineca_Accounting/accounting-saldo.out .
scp boccali@bastion.cnaf.infn.it:/data/CMS/boccali/Cineca_Accounting/jobs\*.out .
scp boccali@bastion.cnaf.infn.it:/data/CMS/boccali/Cineca_Accounting/statscms .
cat statscms |sort|uniq -c |sort -n|tail -n 5
python3 accounting-saldo.py
tail -n 10 jobs.out


