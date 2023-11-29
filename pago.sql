SELECT TO_CHAR(PCPREST.DTPAG, 'YYYY-MM-DD') AS DATAPAGAMENTO,
       PCPREST.CODFILIAL,
       SUM(PCPREST.VALOR)                    AS VALORTITULO,
       SUM(PCPREST.VPAGO)                    AS VALORPAGO,
       SUM(PCPREST.TXPERM)                   AS VALORJUROS,
       SUM(PCPREST.VLTXBOLETO)               AS VLTXBOLETO
FROM PCPREST
GROUP BY TO_CHAR(PCPREST.DTPAG, 'YYYY-MM-DD'),
         PCPREST.CODFILIAL
