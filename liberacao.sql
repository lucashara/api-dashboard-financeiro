SELECT CODFILIAL,
       DTLIBERA,
       EXTRACT(HOUR FROM CAST(DTLIBERA AS TIMESTAMP))  AS HORA_LIBERA,
       DTPED                                           AS DATA_PEDIDO,
       EXTRACT(HOUR FROM CAST(DTPED AS TIMESTAMP))     AS HORA_PEDIDO,
       COUNT(NUMPED)                                   AS QT_PED,
       COUNT(CASE WHEN POSICAO <> 'B' THEN NUMPED END) AS QT_PED_LIB,
       COUNT(CASE WHEN POSICAO = 'B' THEN NUMPED END)  AS QT_PED_BLOQ
FROM (SELECT PCPEDC.CODFILIAL,
             PCPEDC.DTLIBERA,
             NVL(PCPEDC.DTFECHAMENTOPEDPALM, PCPEDC.DTFIMDIGITACAOPEDIDO) AS DTPED,
             PCPEDC.POSICAO,
             PCPEDC.NUMPED
      FROM PCPEDC
      WHERE 
      NVL(PCPEDC.DTFECHAMENTOPEDPALM, PCPEDC.DTFIMDIGITACAOPEDIDO) BETWEEN TRUNC(SYSDATE, 'MM') AND LAST_DAY(TRUNC(SYSDATE, 'MM')) AND
      --NVL(PCPEDC.DTFECHAMENTOPEDPALM, PCPEDC.DTFIMDIGITACAOPEDIDO) >= TRUNC(SYSDATE)

       (PCPEDC.POSICAO = 'B' OR (PCPEDC.POSICAO <> 'B' AND PCPEDC.CODFUNCLIBERA IS NOT NULL)))
GROUP BY CODFILIAL, DTLIBERA, DTPED
