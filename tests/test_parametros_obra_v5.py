"""Testes da integracao parametros_obra <-> registro de tipos (V5).

Cobre a retrocompatibilidade (configs V3/V4 sem os campos novos continuam
validos) e as faixas novas (formatos_lm, modo_producao, cta_url).
"""

import json

import pytest

import parametros_obra as PO
import tipos_obra as TO
from conftest import carregar_script
from nomes_curtos import excede_max_path

fatiar = carregar_script("fatiar-obra.py")


def config_livro(**sobrepor):
    base = {
        "tema": "Obra", "tipo_obra": "livro",
        "min_referencias_por_capitulo": 8, "tamanho_obra": "M",
        "senioridade_obra": "intermediario",
        "cor_primaria": "#58a6ff",
        "subtitulo": "Subtítulo da obra",
        "edition_tag": "v1.0",
    }
    base.update(sobrepor)
    return base


class TestRegistroPropagado:
    def test_tipos_validos_vem_do_registro(self):
        assert PO.TIPOS_VALIDOS == TO.tipos_validos()
        assert "playbook" in PO.TIPOS_VALIDOS
        assert "lead-magnet" in PO.TIPOS_VALIDOS

    def test_perguntaveis_sao_livro_tcc_e_manual_diario(self):
        assert set(PO.TIPOS_PERGUNTAVEIS) == {"livro", "tcc", "manual-diario"}

    def test_defaults_por_tipo_cobre_todos_os_tipos(self):
        assert set(PO.DEFAULTS_POR_TIPO) == set(TO.tipos_validos())
        assert PO.DEFAULTS_POR_TIPO["playbook"]["min_refs"] == 0
        assert PO.DEFAULTS_POR_TIPO["tcc"]["min_refs"] == 8

    def test_citacao_autor_data_delega_ao_registro(self):
        assert PO.usa_citacao_autor_data("tcc") is True
        assert PO.usa_citacao_autor_data("livro") is False


class TestCarregarConfig:
    def test_config_v3_ausente_ganha_campos_v5(self, tmp_path, monkeypatch):
        monkeypatch.setattr(PO, "DIR_OUTPUT", tmp_path)
        cfg = PO.carregar_config("livros/inexistente")
        for chave in PO.DERIVADOS_V5:
            assert chave in cfg
        assert cfg["modo_producao"] == "obra-unica"

    def test_config_v4_existente_ganha_campos_v5_por_setdefault(self, tmp_path, monkeypatch):
        monkeypatch.setattr(PO, "DIR_OUTPUT", tmp_path)
        dir_obra = tmp_path / "livros" / "obra"
        dir_obra.mkdir(parents=True)
        (dir_obra / "config_obra.json").write_text(
            json.dumps(config_livro()), encoding="utf-8")
        cfg = PO.carregar_config("livros/obra")
        assert cfg["gerar_playbook"] is False
        assert cfg["formatos_lm"] == []
        assert cfg["tamanho_obra"] == "M"          # nao sobrescreve o que ja existia

    def test_listas_padrao_nao_sao_compartilhadas(self, tmp_path, monkeypatch):
        monkeypatch.setattr(PO, "DIR_OUTPUT", tmp_path)
        a = PO.carregar_config("livros/a")
        b = PO.carregar_config("livros/b")
        a["formatos_lm"].append("checklist")
        assert b["formatos_lm"] == []

    def test_gerar_campanha_e_gerar_maquina_default_false(self, tmp_path, monkeypatch):
        monkeypatch.setattr(PO, "DIR_OUTPUT", tmp_path)
        cfg = PO.carregar_config("livros/inexistente")
        assert cfg["gerar_campanha"] is False
        assert cfg["gerar_maquina"] is False

    def test_gerar_campanha_e_gerar_maquina_explicitos_sao_preservados(
            self, tmp_path, monkeypatch):
        monkeypatch.setattr(PO, "DIR_OUTPUT", tmp_path)
        dir_obra = tmp_path / "livros" / "obra"
        dir_obra.mkdir(parents=True)
        dados = config_livro()
        dados["gerar_campanha"] = True
        dados["gerar_maquina"] = True
        (dir_obra / "config_obra.json").write_text(
            json.dumps(dados), encoding="utf-8")
        cfg = PO.carregar_config("livros/obra")
        assert cfg["gerar_campanha"] is True
        assert cfg["gerar_maquina"] is True


class TestValidarConfig:
    def test_config_v4_continua_valido(self):
        assert PO.validar_config(config_livro()) == []

    def test_tipo_desconhecido_para_a_validacao(self):
        erros = PO.validar_config(config_livro(tipo_obra="revista"))
        assert len(erros) == 1 and "invalido" in erros[0]

    def test_derivado_nao_e_barrado_por_ser_derivado(self):
        cfg = TO.defaults_config("playbook", slug_mae_simples="obra")
        cfg["senioridade_obra"] = "intermediario"
        assert PO.validar_config(cfg) == []

    def test_playbook_nao_exige_referencias(self):
        cfg = TO.defaults_config("playbook", slug_mae_simples="obra")
        cfg["senioridade_obra"] = "intermediario"
        assert not any("referencias" in e for e in PO.validar_config(cfg))

    def test_fase0_exige_pelo_menos_5_referencias(self):
        erros = PO.validar_config(config_livro(min_referencias_por_capitulo=3))
        assert any("entre 5 e 20" in e for e in erros)

    def test_formatos_lm_invalido_reprova(self):
        erros = PO.validar_config(config_livro(
            gerar_lead_magnets=True, formatos_lm=["checklist", "poster"]))
        assert any("poster" in e for e in erros)

    def test_formatos_lm_vazio_reprova(self):
        erros = PO.validar_config(config_livro(gerar_lead_magnets=True, formatos_lm=[]))
        assert any("formatos_lm" in e for e in erros)

    def test_formatos_lm_validos_passam(self):
        assert PO.validar_config(config_livro(
            gerar_lead_magnets=True, formatos_lm=["checklist", "armadilhas"])) == []

    def test_modo_producao_invalido_reprova(self):
        erros = PO.validar_config(config_livro(modo_producao="turbo"))
        assert any("modo_producao" in e for e in erros)

    def test_estilo_tecnica_invalido_reprova(self):
        erros = PO.validar_config(config_livro(estilo_tecnica="caveman"))
        assert any("estilo_tecnica" in e for e in erros)

    def test_estilo_tecnica_validos_passam(self):
        for modo in ("codigo", "hibrido", "operacional"):
            assert PO.validar_config(config_livro(estilo_tecnica=modo)) == []

    def test_cascata_exige_obra_raiz_valida(self):
        erros = PO.validar_config(config_livro(modo_producao="cascata"))
        assert any("obra_raiz" in e for e in erros)
        assert PO.validar_config(config_livro(modo_producao="cascata",
                                              obra_raiz="tcc")) == []

    def test_cascata_rejeita_raiz_derivada(self):
        erros = PO.validar_config(config_livro(modo_producao="cascata",
                                               obra_raiz="playbook"))
        assert any("obra_raiz" in e for e in erros)

    def test_tipo_de_conversao_exige_cta(self):
        cfg = TO.defaults_config("lead-magnet", slug_mae_simples="obra")
        cfg["senioridade_obra"] = "intermediario"
        assert any("cta_url" in e for e in PO.validar_config(cfg))
        cfg["cta_url"] = "https://exemplo.com"
        assert PO.validar_config(cfg) == []

    def test_playbook_nao_exige_cta(self):
        cfg = TO.defaults_config("playbook", slug_mae_simples="obra")
        cfg["senioridade_obra"] = "intermediario"
        assert not any("cta_url" in e for e in PO.validar_config(cfg))


class TestFatiarObraPlaybook:
    @pytest.fixture
    def ambiente(self, livro_falso, monkeypatch):
        monkeypatch.setattr(fatiar, "DIR_OUTPUT", livro_falso["raiz"])
        return livro_falso

    def _dir_playbook(self, ambiente):
        """Caminho V5.1 do playbook: playbooks/<codigo-obra>/pbk-1-<nome>."""
        slug = TO.slug_curto("playbook", "obra-teste", nome="A Obra em Construção")
        return ambiente["raiz"] / slug

    def test_cria_esqueleto_do_playbook(self, ambiente):
        assert fatiar.gerar_playbook(ambiente["slug"]) == 0
        dir_pbk = self._dir_playbook(ambiente)
        assert (dir_pbk / "config_obra.json").exists()
        assert (dir_pbk / "passos").is_dir()

    def test_caminho_gerado_cabe_no_max_path(self, ambiente):
        fatiar.gerar_playbook(ambiente["slug"])
        assert not excede_max_path(self._dir_playbook(ambiente))

    def test_encurta_de_verdade_quando_a_obra_tem_nome_longo(self, tmp_path, monkeypatch):
        """A convencao V5.1 existe para o caso REAL. Com um slug ja curto o ganho
        e nulo (ate negativo); o que ela resolve e o nome de obra de 42 chars
        repetido na pasta E no arquivo, que gerava caminhos de ~197."""
        # Layout plano: sem obra-root no output (serie-aware encontraria a real).
        monkeypatch.setattr(TO, "DIR_OUTPUT", tmp_path / "output")
        mae = "ai-driven-development-do-zero-ao-deploy-v2"
        antigo = f"playbooks/{mae}--pbk/{mae}--pbk.pdf"      # 109 chars
        slug = TO.slug_curto("playbook", mae, nome="AI Driven Development")
        novo = f"{slug}/{TO.nome_arquivo(slug)}.pdf"          # 79 chars
        assert len(novo) <= len(antigo) * 0.75, f"{len(novo)} vs {len(antigo)}"
        # Nenhum segmento pode carregar o slug inteiro da obra-mae
        assert max(len(s) for s in novo.split("/")) <= 32, novo

    def test_herda_senioridade_serie_e_motivo_condutor(self, ambiente):
        fatiar.gerar_playbook(ambiente["slug"])
        dir_pbk = self._dir_playbook(ambiente)
        cfg = json.loads((dir_pbk / "config_obra.json").read_text(encoding="utf-8"))
        sumario = json.loads((dir_pbk / "sumario_macro.json").read_text(encoding="utf-8"))
        assert cfg["senioridade_obra"] == "intermediario"
        assert cfg["serie"] == "Colecao Teste"
        assert sumario["motivo_condutor"]["persona_leitor"] == "Mestre de Obras"

    def test_estagios_usam_o_vocabulario_condutor(self, ambiente):
        fatiar.gerar_playbook(ambiente["slug"])
        sumario = json.loads((self._dir_playbook(ambiente) / "sumario_macro.json")
                             .read_text(encoding="utf-8"))
        assert sumario["estagios"][0]["nome"] == "Fundação"

    def test_registra_em_derivados_json(self, ambiente):
        fatiar.gerar_playbook(ambiente["slug"])
        derivados = json.loads((ambiente["dir_livro"] / "derivados.json")
                               .read_text(encoding="utf-8"))
        assert derivados["playbooks"]["total"] == 1
        item = derivados["playbooks"]["itens"][0]
        assert item["slug"] == "pbk-1-obra-construcao"
        assert (ambiente["raiz"] / item["diretorio"]).is_dir()

    def test_preserva_secoes_de_outros_derivados(self, ambiente):
        (ambiente["dir_livro"] / "derivados.json").write_text(json.dumps({
            "slug_livro_mae": "obra-teste",
            "artigos": {"total": 2, "itens": [{"indice": 1}, {"indice": 2}]},
        }), encoding="utf-8")
        fatiar.gerar_playbook(ambiente["slug"])
        derivados = json.loads((ambiente["dir_livro"] / "derivados.json")
                               .read_text(encoding="utf-8"))
        assert derivados["artigos"]["total"] == 2
        assert derivados["playbooks"]["total"] == 1

    def test_carregar_derivados_cria_secao_por_tipo_derivado(self, ambiente):
        base = fatiar.carregar_derivados(ambiente["dir_livro"])
        for tipo in TO.tipos_derivados():
            assert TO.raiz_output(tipo) in base

    def test_obra_sem_sumario_falha(self, ambiente):
        (ambiente["dir_livro"] / "sumario_macro.json").unlink()
        assert fatiar.gerar_playbook(ambiente["slug"]) == 1

    def test_derivacao_invalida_e_barrada(self, ambiente):
        caminho = ambiente["dir_livro"] / "config_obra.json"
        cfg = json.loads(caminho.read_text(encoding="utf-8"))
        cfg["tipo_obra"] = "tcc"
        caminho.write_text(json.dumps(cfg, ensure_ascii=False), encoding="utf-8")
        assert fatiar.gerar_playbook(ambiente["slug"]) == 1
