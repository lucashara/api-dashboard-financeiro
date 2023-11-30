SELECT PCPREST.CODFILIAL,
       SUM(CASE
               WHEN PCPREST.DTPAG IS NULL AND
                    PCPREST.CODCOB NOT IN ('DEVP', 'DEVT', 'BNF', 'BNFT', 'BNFR', 'BNTR', 'BNRP', 'CRED')
                   THEN PCPREST.VALOR - NVL(PCPREST.VALORDESC, 0)
               ELSE 0
           END) AS VALORARECEBER
FROM PCPREST
WHERE (CASE
           WHEN PCPREST.DTPAG IS NULL AND
                PCPREST.CODCOB NOT IN ('DEVP', 'DEVT', 'BNF', 'BNFT', 'BNFR', 'BNTR', 'BNRP', 'CRED')
               THEN PCPREST.VALOR - NVL(PCPREST.VALORDESC, 0)
           ELSE 0
    END) > 0
  AND PCPREST.DTVENC BETWEEN TO_DATE(:DATAINICIAL, 'DD-MM-YYYY') AND TO_DATE(:DATAFINAL, 'DD-MM-YYYY')
GROUP BY PCPREST.CODFILIAL