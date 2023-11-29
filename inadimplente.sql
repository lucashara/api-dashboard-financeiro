SELECT TO_CHAR(PCPREST.DTVENC, 'YYYY-MM-DD') AS DATAVENCIMENTO,
       PCPREST.CODFILIAL,
       CASE
           WHEN PCPREST.DTPAG IS NULL AND PCPREST.DTVENC < TRUNC(SYSDATE) THEN 'INADIMPLENTE'
           ELSE 'ADIMPLENTE'
           END                               AS INADIMPLENCIA,
       SUM(PCPREST.VALOR)                    AS VALORTITULO
FROM PCPREST
GROUP BY TO_CHAR(PCPREST.DTVENC, 'YYYY-MM-DD'),
         PCPREST.CODFILIAL,
         CASE
             WHEN PCPREST.DTPAG IS NULL AND PCPREST.DTVENC < TRUNC(SYSDATE) THEN 'INADIMPLENTE'
             ELSE 'ADIMPLENTE'
             END
