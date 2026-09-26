# Vern ר�� Codex / Plugin ������

�װ� 0.1.0���� Vern �� SOP���о�����Ŀ����վ�����顢Excel �Ͳ�Ʒ���������������߸��ɸ��� Skills���ȿ��ڱ��ֿ����� Codex ��ȡ��Ҳ��ͨ���ֿ� marketplace ��װ���������**�ֿⴴ�������ڱ����Ѿ���װ���ⲿ�����ѽ�ͨ��**

## �Ѱ���������

| Skill | ��Ҫ��; |
|---|---|
| [vern-sop](plugins/vern-workspace/skills/vern-sop/SKILL.md) | SOP ����ҵ���� |
| [vern-market-insight](plugins/vern-workspace/skills/vern-market-insight/SKILL.md) | �г������������֤ |
| [vern-project-coordination](plugins/vern-workspace/skills/vern-project-coordination/SKILL.md) | ��Ŀͳ������ȹ��� |
| [vern-website-seo](plugins/vern-workspace/skills/vern-website-seo/SKILL.md) | ��վ������ SEO |
| [vern-meeting-minutes](plugins/vern-workspace/skills/vern-meeting-minutes/SKILL.md) | �����Ҫ���ж��ջ� |
| [vern-excel-dashboard](plugins/vern-workspace/skills/vern-excel-dashboard/SKILL.md) | Excel �뾭Ӫ���� |
| [vern-product-development](plugins/vern-workspace/skills/vern-product-development/SKILL.md) | ��Ʒ������׶��� |

ÿ������������������롢ִ�з�����������顢�ɵ����Ľ����ṹ�� UI Ԫ���ݡ�Ĭ�������������Զ�ƥ�䣻ֻ������� Skill��

## Ŀ¼

```text
Vern/
������ .agents/plugins/marketplace.json
������ AGENTS.md
������ README.md
������ tests/test_workspace.py
������ plugins/vern-workspace/
    ������ plugin.json
    ������ .codex-plugin/plugin.json
    ������ README.md
    ������ skills/<skill-name>/
    ��   ������ SKILL.md
    ��   ������ agents/openai.yaml
    ��   ������ references/deliverable.md
    ������ references/
    ��   ������ working-principles.md
    ��   ������ evidence-standard.md
    ��   ������ task-data-contract.md
    ��   ������ official-sources.md
    ��   ������ acceptance-cases.md
    ��   ������ integrations/{README.md,registry.json}
    ������ assets/templates/{brief.md,tasks.csv,evidence.csv}
    ������ scripts/{validate_workspace.py,new_case.py}
```

## ʹ��

### �ڵ�ǰ�ֿ�ʹ��
�Ѳֿ��¡/���ص��ɷ���Ŀ¼���� Codex �д�����δ��װ���ʱ��ֱ��Ҫ�󣺡���ȡ `plugins/vern-workspace/skills/vern-sop/SKILL.md`�����䷽���������ṩ�����̡����� AGENTS.md �������Լ����

### ��װ�������
��֧�� Plugin marketplace �� Codex CLI ����������ֿ���Դ��

```shell
codex plugin marketplace add Vern-maker/Vern --ref main
codex plugin marketplace list
```

Ȼ����Ӧ�õ� Plugins Directory ��ѡ�����Դ����װ `vern-workspace`���������������á����б�δ���£�ˢ��/����Ӧ�á���ǰ�ɹٷ� scaffold ���ɵ� marketplace ��ʶΪ `personal`����ʾ��Ϊ `Personal`���� `marketplace list` �˶�����Դ�Ǳ��ֿ⣬����������ͬ����Դ������������ͬ�� marketplace������ά���߰��ٷ����̵����ֿ� catalog ��ʶ�������ӣ������Ǹ������á�

��װ��ɰ�����ʹ�� `@` �� `$` ѡ����Ӧ Skill�����磺

```text
�� $vern-meeting-minutes �������תд�������Ѿ���������ʹ�ȷ�ϡ�
�� $vern-project-coordination ����Щ��Ŀ������ͬһ������̨�����ܱ���
�� $vern-excel-dashboard ����̨�������ɱ༭���壬˵����ʽ�͸��·�����
```

���汾�İ�װ����/����ɱ仯���� [�ٷ��淶����Դ](plugins/vern-workspace/references/official-sources.md)����Ҫ���߸� Skill �������Ƶ�ȫ��Ŀ¼���ְ�װ������������ظ���ں͹������öϿ���

## ���ع���

Python 3.10+������׼�⣻�Ӳֿ��Ŀ¼���У�

```shell
python plugins/vern-workspace/scripts/validate_workspace.py
python -m unittest discover -s tests
python plugins/vern-workspace/scripts/new_case.py sample-project --root cases
```

���һ������ȷ�� cases Ŀ¼�����򱨡�����/֤�ݿձ��Լ� inputs/work/outputs ��Ŀ¼������ͬ��Ŀ¼��ֹͣ�����������ϡ�δ�Զ�����ҵ����ʵ��

У�麭�Ǳ��ֿ���õ� manifest �ֶΡ�����һ���ԡ����� Skill������·����UI ��Ϣ����չλ�����ǹٷ����� schema У���ҵ��������֤��ҵ�����ռ� [��������](plugins/vern-workspace/references/acceptance-cases.md)��

## ��������

Mermaid��MarkItDown��n8n��Firecrawl��Plane ������ [�滮���](plugins/vern-workspace/references/integrations/README.md)����ǰȫ�� `planned` / `enabled: false`��û�������Զ�ץȡ����ʱ���ѡ��˺š��շѷ�����ⲿ����ͬ����

��������һ����ʵ���̡�һ�ݻ����¼��һ������̨�����ã��������������ٰ�ʵ����Ҫ���빤�ߡ�ҵ�����Ϸ�˽�й������������ֿⱣ������������ģ�塣

## ά��

- �޸� Skill ʱͬ�����ģ�����������Ӱ�췶Χ���գ����ѻ������ͻ�Ĺ���
- �����°汾ʱͬ������ plugin manifest �İ汾������У�飬���°�װ/ˢ�º�����������֤����Ҫֻ��Դ�ļ��������Ѹ��°�װ���档
- ��˾ģ�塢�����Ʒ��֤���Ժ��貹�룻δ����������ݲ���д�ɹ�˾��ʵ��
- ��δָ����Դ����֤������������Ȩ�����ɲֿ������߾�����
