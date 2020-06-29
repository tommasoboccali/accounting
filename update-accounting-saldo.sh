#scp tboccali@login.marconi.cineca.it:/marconi_work/Pra18_4658/accounting/accounting-saldo.out .
scp boccali@bastion.cnaf.infn.it:/data/CMS/boccali/Cineca_Accounting/accounting-saldo.out .
scp boccali@bastion.cnaf.infn.it:/data/CMS/boccali/Cineca_Accounting/jobs\*.out .
python3 accounting-saldo.py

