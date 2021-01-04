#scp tboccali@login.marconi.cineca.it:/marconi_work/Pra18_4658/accounting/accounting-saldo.out .
rm -f accounting-saldo.out jobs.out statcms2
scp boccali@bastion.cnaf.infn.it:/data/CMS/boccali/Cineca_Accounting/accounting-saldo.out .
scp boccali@bastion.cnaf.infn.it:/data/CMS/boccali/Cineca_Accounting/jobs\*.out .

#scp boccali@bastion.cnaf.infn.it:/data/CMS/boccali/Cineca_Accounting/statscms .
scp boccali@bastion.cnaf.infn.it:/data/CMS/boccali/Cineca_Accounting/statscms2 .
echo ==== CMS Workflows
cat statscms2 |sort|uniq -c |sort -n|tail -n 5
echo ==================
python3 accounting-saldo.py
tail -n 10 jobs.out


