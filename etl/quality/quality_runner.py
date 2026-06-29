import getpass

from datetime import datetime

from etl.utils.db_connection import get_connection


conn = get_connection()

cursor = conn.cursor()

processo = "quality_runner"

tabela = "quality.data_quality_log"

data_inicio = datetime.now()

linhas_inseridas = 0


def registrar_validacao(
    tabela,
    regra,
    resultado,
    qtd_registros,
    observacao=None
):
    cursor.execute(
        """
        INSERT INTO quality.data_quality_log (
            tabela,
            regra,
            resultado,
            qtd_registros,
            observacao
        )
        VALUES (%s,%s,%s,%s,%s)
        """,
        (
            tabela,
            regra,
            resultado,
            qtd_registros,
            observacao
        )
    )


try:

    cursor.execute(
        """
        INSERT INTO audit.etl_run_log (
            processo,
            tabela,
            status,
            data_inicio,
            usuario_execucao
        )
        VALUES (%s,%s,%s,%s,%s)
        RETURNING id
        """,
        (
            processo,
            tabela,
            "RUNNING",
            data_inicio,
            getpass.getuser()
        )
    )

    log_id = cursor.fetchone()[0]

    conn.commit()

    print("Iniciando validações de qualidade...")

    # =====================================================
    # 1 - Atendimentos sem profissional
    # =====================================================

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM silver.atendimentos
        WHERE id_profissional IS NULL
        """
    )

    qtd = cursor.fetchone()[0]

    registrar_validacao(
        tabela="silver.atendimentos",
        regra="id_profissional_nao_nulo",
        resultado="PASS" if qtd == 0 else "FAIL",
        qtd_registros=qtd,
        observacao="Validação de profissional"
    )

    # =====================================================
    # 2 - Atendimentos sem paciente
    # =====================================================

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM silver.atendimentos
        WHERE id_paciente IS NULL
        """
    )

    qtd = cursor.fetchone()[0]

    registrar_validacao(
        tabela="silver.atendimentos",
        regra="id_paciente_nao_nulo",
        resultado="PASS" if qtd == 0 else "FAIL",
        qtd_registros=qtd,
        observacao="Validação de paciente"
    )

    # =====================================================
    # 3 - Receita negativa
    # =====================================================

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM silver.atendimentos
        WHERE receita_bruta < 0
        """
    )

    qtd = cursor.fetchone()[0]

    registrar_validacao(
        tabela="silver.atendimentos",
        regra="receita_nao_negativa",
        resultado="PASS" if qtd == 0 else "FAIL",
        qtd_registros=qtd,
        observacao="Receita deve ser positiva"
    )

    # =====================================================
    # 4 - Faltas sem profissional
    # =====================================================

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM silver.faltas_pacientes
        WHERE id_profissional IS NULL
        """
    )

    qtd = cursor.fetchone()[0]

    registrar_validacao(
        tabela="silver.faltas_pacientes",
        regra="id_profissional_nao_nulo",
        resultado="PASS" if qtd == 0 else "FAIL",
        qtd_registros=qtd,
        observacao="Validação profissional"
    )

    # =====================================================
    # 5 - Snapshot Gold duplicado no mesmo dia
    # =====================================================

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM (
            SELECT
                data_referencia,
                COUNT(*)
            FROM gold.kpi_operacional_snapshot
            GROUP BY data_referencia
            HAVING COUNT(*) > 1
        ) t
        """
    )

    qtd = cursor.fetchone()[0]

    registrar_validacao(
        tabela="gold.kpi_operacional_snapshot",
        regra="snapshot_unico_por_dia",
        resultado="PASS" if qtd == 0 else "FAIL",
        qtd_registros=qtd,
        observacao="Validação de duplicidade"
    )

    conn.commit()

    linhas_inseridas = 5

    data_fim = datetime.now()

    tempo_execucao = (
        data_fim - data_inicio
    ).total_seconds()

    cursor.execute(
        """
        UPDATE audit.etl_run_log
        SET
            status = %s,
            data_fim = %s,
            tempo_execucao_seg = %s,
            linhas_inseridas = %s
        WHERE id = %s
        """,
        (
            "SUCCESS",
            data_fim,
            tempo_execucao,
            linhas_inseridas,
            log_id
        )
    )

    conn.commit()

    print("Validações concluídas com sucesso.")

except Exception as e:

    conn.rollback()

    data_fim = datetime.now()

    tempo_execucao = (
        data_fim - data_inicio
    ).total_seconds()

    try:

        cursor.execute(
            """
            UPDATE audit.etl_run_log
            SET
                status = %s,
                data_fim = %s,
                tempo_execucao_seg = %s,
                mensagem_erro = %s
            WHERE id = %s
            """,
            (
                "ERROR",
                data_fim,
                tempo_execucao,
                str(e),
                log_id
            )
        )

        conn.commit()

    except:
        pass

    print(f"Erro: {e}")

finally:

    cursor.close()

    conn.close()