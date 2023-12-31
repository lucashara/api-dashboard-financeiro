SELECT PCPREST.CODFILIAL,
       SUM(PCPREST.VALOR)      AS VALORTITULO,
       SUM(PCPREST.VPAGO)      AS VALORPAGO,
       SUM(PCPREST.TXPERM)     AS VALORJUROS,
       SUM(PCPREST.VLTXBOLETO) AS VLTXBOLETO
FROM PCPREST
WHERE PCPREST.DTBAIXA BETWEEN TO_DATE(:DATAINICIAL, 'DD-MM-YYYY') AND TO_DATE(:DATAFINAL, 'DD-MM-YYYY')
GROUP BY PCPREST.CODFILIAL
