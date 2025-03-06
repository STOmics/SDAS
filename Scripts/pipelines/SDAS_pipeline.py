import sys,re,os
import argparse

USAGE = 'python3 SDAS_pipeline.py -c pipeline_input.conf -o ./'

def _readconf(conf):
    conf_dict = {}
    with open(conf,'r') as cf:
        for line in cf:
            line = line.strip()
            if not line.startswith('#') and '=' in line:
                lines = line.split('=',1)
                para = lines[0].strip() 
                value = lines[1].strip()
                if value:
                    conf_dict[para] = value
    return conf_dict

def outshell(sh_file, sh_code, cpu, mem):
    outf =  open(sh_file,'w')
    outf.write(sh_code + '\n')
    outf.write('echo "All finished" 1>&2 && \\\n')
    outf.write(f'echo "All finished" > {sh_file}.log\n')
    outf.close()
    sh_flag = f'{sh_file}:cpu:{cpu}:mem:{mem}G'
    return sh_flag

def _h5ad(sdas_conf, outdir):
    os.system(f'mkdir -p {outdir}/input_file/shell {outdir}/input_file/result')
    cpu = 1
    mem = 1
    result_file = ''
    h5ad_sh = f'{outdir}/input_file/shell/merge_h5ads.sh'
    sh_code = ''
    h5ad_files = sdas_conf['h5ad_files'].split(';')
    if len(h5ad_files) == 1:
        sh_code = f'ln -sf {h5ad_files[0]} {outdir}/input_file/result/infile.h5ad && \\'
        result_file = f'{outdir}/input_file/result/infile.h5ad'
    else:
        h5ad_csv = open(f'{outdir}/input_file/result/samples.csv','w')
        h5ad_csv.write('\n'.join(h5ad_files))
        h5ad_csv.close()
        sh_code = f'{sdas_conf["SDAS_software"]} dataProcess input2h5ad -i {outdir}/input_file/result/samples.csv --mode multi -o {outdir}/input_file/result && \\'
        result_file = f'{outdir}/input_file/result/combine_standard.h5ad'
        cpu = 3
        mem = 10
        
    sh_flag = outshell(h5ad_sh, sh_code, cpu, mem)
    shell_list = []
    shell_list.append(sh_flag)
    return result_file,shell_list

def _coexpress(input_file, sdas_conf, outdir):
    os.system(f'mkdir -p {outdir}/coexpress/shell {outdir}/coexpress/result')
    cpu = 3
    mem = 10
    if int(sdas_conf['coexpress_bin_size']) >= 100:
        cpu = 3
        mem = 30
    elif int(sdas_conf['coexpress_bin_size']) >= 50:
        cpu = 5
        mem = 50
    else:
        cpu = 10
        mem = 90
    method = sdas_conf['coexpress_method']
    coexp_sh = f'{outdir}/coexpress/shell/coexpress_{method}.sh'
    sh_code = f'{sdas_conf["SDAS_software"]} coexpress {method} -i {input_file} '
    for p in sdas_conf.keys():
        if p.startswith('coexpress_') or p.startswith(f'{method}_'):
            if p != 'coexpress_method':
                pras = p.split('_',1)
                sh_code += f'--{pras[1]} {sdas_conf[p]} '
            if p == 'coexpress_n_cpus':
                cpu = sdas_conf['coexpress_n_cpus']
    sh_code += f'-o {outdir}/coexpress/result && \\'
    sh_flag = outshell(coexp_sh, sh_code, cpu, mem)
    shell_list = []
    shell_list.append(sh_flag)
    return shell_list

def _cellannotation(input_file, sdas_conf, outdir):
    os.system(f'mkdir -p {outdir}/cellAnnotation/shell {outdir}/cellAnnotation/result')
    cpu = 4
    mem = 20
    if int(sdas_conf['cellanno_bin_size']) >= 100:
        cpu = 4
        mem = 20
    elif int(sdas_conf['cellanno_bin_size']) >= 50:
        cpu = 4
        mem = 80
    else:
        cpu = 10
        mem = 100
    method = sdas_conf['cellanno_method']
    annot_sh = f'{outdir}/cellAnnotation/shell/cellAnnotation_{method}.sh'
    sh_code = f'{sdas_conf["SDAS_software"]} cellAnnotation {method} -i {input_file} '
    for p in sdas_conf.keys():
        if p.startswith('cellanno_') or p.startswith(f'{method}_'):
            if p != 'cellanno_method':
                pras = p.split('_',1)
                sh_code += f'--{pras[1]} {sdas_conf[p]} '
            if p == 'cell2location_n_threads':
                cpu = sdas_conf['cell2location_n_threads']
    sh_code += f'-o {outdir}/cellAnnotation/result && \\'
    sh_flag = outshell(annot_sh, sh_code, cpu, mem)
    shell_list = []
    shell_list.append(sh_flag)
    out_file_name = os.path.basename(input_file)
    out_file_name = re.sub(r'.h5ad','',out_file_name)
    out_file_name = f'{out_file_name}_anno_{method}.h5ad'
    out_file = f'{outdir}/cellAnnotation/result/{out_file_name}'
    return out_file,shell_list

def _spatialDomain(input_file, sdas_conf, outdir):
    os.system(f'mkdir -p {outdir}/spatialDomain/shell {outdir}/spatialDomain/result')
    cpu = 3
    mem = 10
    if int(sdas_conf['spatialDomain_bin_size']) >= 100:
        cpu = 3
        mem = 20
    else:
        cpu = 10
        mem = 100
    method = sdas_conf['spatialDomain_method']
    domain_sh = f'{outdir}/spatialDomain/shell/spatialDomain_{method}.sh'
    sh_code = f'{sdas_conf["SDAS_software"]} spatialDomain {method} -i {input_file} '
    for p in sdas_conf.keys():
        if p.startswith('spatialDomain_') or p.startswith(f'{method}_'):
            if p != 'spatialDomain_method':
                pras = p.split('_',1)
                sh_code += f'--{pras[1]} {sdas_conf[p]} '
    sh_code += f'-o {outdir}/spatialDomain/result && \\'
    sh_flag = outshell(domain_sh, sh_code, cpu, mem)
    shell_list = []
    shell_list.append(sh_flag)
    out_file_name = os.path.basename(input_file)
    out_file_name = re.sub(r'.h5ad','',out_file_name)
    out_file_name = f'{out_file_name}_{method}.h5ad'
    out_file = f'{outdir}/spatialDomain/result/{out_file_name}'
    return out_file,shell_list

def _infercnv(cell_anno, sdas_conf, outdir):
    os.system(f'mkdir -p {outdir}/infercnv/shell {outdir}/infercnv/result')
    cpu = 3
    mem = 20
    anno_file = os.path.basename(cell_anno)
    anno_file = re.sub(r'.h5ad','',anno_file)
    cnv_sh = f'{outdir}/infercnv/shell/infercnv.sh'
    sh_code = f'{sdas_conf["SDAS_software"]} dataProcess h5ad2rds -i {cell_anno} -o {outdir}/infercnv/result && \\\n'
    sh_code += f'{sdas_conf["SDAS_software"]} infercnv -i {outdir}/infercnv/result/{anno_file}.rds --h5ad {cell_anno} '
    for p in sdas_conf.keys():
        if p.startswith('infercnv_'):
            pras = p.split('_',1)
            sh_code += f'--{pras[1]} {sdas_conf[p]} '
    sh_code += f'-o {outdir}/infercnv/result && \\'
    sh_flag = outshell(cnv_sh, sh_code, cpu, mem)
    shell_list = []
    shell_list.append(sh_flag)
    return shell_list

def _CCI(cell_anno, sdas_conf, outdir):
    os.system(f'mkdir -p {outdir}/cci/shell {outdir}/cci/result')
    cpu = 3
    mem = 10
    if int(sdas_conf['cellchat_bin_size']) >= 100:
        cpu = 3
        mem = 20
    elif int(sdas_conf['cellchat_bin_size']) >= 20:
        cpu = 4
        mem = 50
    else:
        cpu = 10
        mem = 200
    anno_file = os.path.basename(cell_anno)
    anno_file = re.sub(r'.h5ad','',anno_file)
    method = sdas_conf['CCI_method']
    cci_sh = f'{outdir}/cci/shell/cci_{method}.sh'
    sh_code = f'{sdas_conf["SDAS_software"]} dataProcess h5ad2rds -i {cell_anno} -o {outdir}/cci/result && \\\n'
    sh_code += f'{sdas_conf["SDAS_software"]} CCI {method} -i {outdir}/cci/result/{anno_file}.rds '
    for p in sdas_conf.keys():
        if p.startswith('CCI_') or p.startswith(f'{method}_'):
            if p != 'CCI_method':
                pras = p.split('_',1)
                sh_code += f'--{pras[1]} {sdas_conf[p]} '
    sh_code += f'-o {outdir}/cci/result && \\'
    sh_flag = outshell(cci_sh, sh_code, cpu, mem)
    shell_list = []
    shell_list.append(sh_flag)
    return shell_list

def _trajectory(cell_anno, sdas_conf, outdir):
    os.system(f'mkdir -p {outdir}/trajectory/shell {outdir}/trajectory/result')
    cpu = 3
    mem = 50
    anno_file = os.path.basename(cell_anno)
    anno_file = re.sub(r'.h5ad','',anno_file)
    method = sdas_conf['trajectory_method']
    traj_sh = f'{outdir}/trajectory/shell/trajectory_{method}.sh'
    sh_code = f'{sdas_conf["SDAS_software"]} dataProcess h5ad2rds -i {cell_anno} -o {outdir}/trajectory/result && \\\n'
    sh_code += f'{sdas_conf["SDAS_software"]} trajectory {method} -i {outdir}/trajectory/result/{anno_file}.rds '
    for p in sdas_conf.keys():
        if p.startswith('trajectory_') or p.startswith(f'{method}_'):
            if p != 'trajectory_method':
                pras = p.split('_',1)
                sh_code += f'--{pras[1]} {sdas_conf[p]} '
    sh_code += f'-o {outdir}/trajectory/result && \\'
    sh_flag = outshell(traj_sh, sh_code, cpu, mem)
    shell_list = []
    shell_list.append(sh_flag)
    return shell_list

def _deg(st_domain, sdas_conf, outdir):
    os.system(f'mkdir -p {outdir}/deg/shell {outdir}/deg/result')
    cpu = 1
    mem = 2
    diff_plans = sdas_conf['deg_plan'].split(';')
    diff_plan_file = open(f'{outdir}/deg/result/diff_plan.csv','w')
    diff_plan_file.write('\n'.join(diff_plans))
    diff_plan_file.close()
    deg_sh = f'{outdir}/deg/shell/deg.sh'
    deg_code = f'{sdas_conf["SDAS_software"]} DEG -i {st_domain} --diff_plan {outdir}/deg/result/diff_plan.csv '
    for p in sdas_conf.keys():
        if p.startswith('deg_') :
            if p != 'deg_plan':
                pras = p.split('_',1)
                deg_code += f'--{pras[1]} {sdas_conf[p]} '
    deg_code += f'-o {outdir}/deg/result && \\'
    sh_flag = outshell(deg_sh, deg_code, cpu, mem)
    shell_list = []
    shell_list.append(sh_flag)
    diff_dir = f'{outdir}/deg/result'
    return diff_dir,shell_list

def _degEnrich(deg_result_dir, sdas_conf, outdir):
    os.system(f'mkdir -p {outdir}/geneEnrichment/shell {outdir}/geneEnrichment/result')
    cpu = 1
    mem = 2
    paras = ''
    for p in sdas_conf.keys():
        if p.startswith('geneSetEnrichment_') :
            pras = p.split('_',1)
            paras += f'--{pras[1]} {sdas_conf[p]} '
    enrich_shell = f'''
for dif in $(ls {deg_result_dir}/*.deg_filtered.csv)
do
    filename=$(basename "$dif" .deg_filtered.csv)
    {sdas_conf["SDAS_software"]} geneSetEnrichment enrichr -i $dif {paras} -o {outdir}/geneEnrichment/result/$filename
done
'''
    enrich_shell += f'''
for dif in $(ls {deg_result_dir}/*.deg.csv)
do
    filename=$(basename "$dif" .deg.csv)
    {sdas_conf["SDAS_software"]} geneSetEnrichment prerank -i $dif {paras} -o {outdir}/geneEnrichment/result/$filename
done
'''
    enrich_file = f'{outdir}/geneEnrichment/shell/deg_enrich.sh'
    sh_flag = outshell(enrich_file, enrich_shell, cpu, mem)
    shell_list = []
    shell_list.append(sh_flag)
    return shell_list

def _gsea(st_domain, sdas_conf, outdir):
    os.system(f'mkdir -p {outdir}/geneEnrichment/shell {outdir}/geneEnrichment/result')
    cpu = 1
    mem = 2
    gsea_plans = sdas_conf['gsea_plan'].split(';')
    gsea_plan_file = open(f'{outdir}/geneEnrichment/result/gsea_plan.csv','w')
    gsea_plan_file.write('\n'.join(gsea_plans))
    gsea_plan_file.close()
    gsea_sh = f'{outdir}/geneEnrichment/shell/gsea.sh'
    sh_code = f'{sdas_conf["SDAS_software"]} geneSetEnrichment gsea -i {st_domain} --gsea_plan {outdir}/geneEnrichment/result/gsea_plan.csv '
    for p in sdas_conf.keys():
        if p.startswith('geneSetEnrichment_') or p.startswith('gsea_'):
            if p != 'gsea_plan':
                pras = p.split('_',1)
                sh_code += f'--{pras[1]} {sdas_conf[p]} '
    sh_code += f'-o {outdir}/geneEnrichment/result && \\'
    sh_flag = outshell(gsea_sh, sh_code, cpu, mem)
    shell_list = []
    shell_list.append(sh_flag)
    return shell_list

def _gsva(st_domain, sdas_conf, outdir):
    os.system(f'mkdir -p {outdir}/geneEnrichment/shell {outdir}/geneEnrichment/result')
    cpu = 1
    mem = 2
    gsva_plans = sdas_conf['gsva_plan'].split(';')
    gsva_plan_file = open(f'{outdir}/geneEnrichment/result/gsva_plan.csv','w')
    for plan in gsva_plans:
        plan = re.sub(r':',';',plan)
        gsva_plan_file.write(f'{plan}\n')
    gsva_plan_file.close()
    gsva_sh = f'{outdir}/geneEnrichment/shell/gsva.sh'
    sh_code = f'{sdas_conf["SDAS_software"]} geneSetEnrichment gsva -i {st_domain} --gsva_plan {outdir}/geneEnrichment/result/gsva_plan.csv '
    for p in sdas_conf.keys():
        if p.startswith('geneSetEnrichment_') or p.startswith('gsva_'):
            if p != 'gsva_plan':
                pras = p.split('_',1)
                sh_code += f'--{pras[1]} {sdas_conf[p]} '
    sh_code += f'-o {outdir}/geneEnrichment/result && \\'
    sh_flag = outshell(gsva_sh, sh_code, cpu, mem)
    shell_list = []
    shell_list.append(sh_flag)
    return shell_list

def main():
    parser = argparse.ArgumentParser(usage=USAGE)
    sub_parsers = parser.add_subparsers(help="Commands help.")
    parser.add_argument("-c","--conf", action="store", type=str, dest="conf",help="input conf file")
    parser.add_argument("-o","--outdir", action="store", type=str, default="./", dest="outdir", help="output directory")
    args = parser.parse_args()

    outdir = os.path.abspath(args.outdir)
    sdas_conf = _readconf(args.conf)
    
    if 'SDAS_software' not in sdas_conf.keys():
        print('SDAS_software not in conf file, please set')
        sys.exit(1)
    if 'h5ad_files' not in sdas_conf.keys():
        print('h5ad_files not in conf file, please set')
        sys.exit(1)
    if 'process' not in sdas_conf.keys():
        print('process not in conf file, please set')
        sys.exit(1)

    os.system(f'mkdir -p {outdir}')
    outshell = open(f'{outdir}/all_shell.conf','w')
    process = sdas_conf['process'].split(',')
    in_files_num = len(sdas_conf['h5ad_files'].split(';'))

    input_file,h5ad_shs = _h5ad(sdas_conf, outdir)

    if in_files_num == 1:
        if 'coexpress' in process:
            coexp_shs = _coexpress(input_file, sdas_conf, outdir)
            for esh in coexp_shs:
                for h5sh in h5ad_shs:
                    outshell.write(f'{h5sh}\t{esh}\n')

    if 'cellAnnotation' in process:
        cell_anno,anno_shs = _cellannotation(input_file, sdas_conf, outdir)
        for ansh in anno_shs:
            for h5sh in h5ad_shs:
                outshell.write(f'{h5sh}\t{ansh}\n')

    if 'spatialDomain' in process:
        st_domain,domain_shs = _spatialDomain(input_file, sdas_conf, outdir)
        for domsh in domain_shs:
            for h5sh in h5ad_shs:
                outshell.write(f'{h5sh}\t{domsh}\n')

    if 'infercnv' in process:
        cnv_shs = _infercnv(cell_anno, sdas_conf, outdir)
        for csh in cnv_shs:
            for ansh in anno_shs:
                outshell.write(f'{ansh}\t{csh}\n')

    if 'CCI' in process:
        cci_shs = _CCI(cell_anno, sdas_conf, outdir)
        for ccsh in cci_shs:
            for ansh in anno_shs:
                outshell.write(f'{ansh}\t{ccsh}\n')

    if 'trajectory' in process:
        traj_shs = _trajectory(cell_anno, sdas_conf, outdir)
        for tsh in traj_shs:
            for ansh in anno_shs:
                outshell.write(f'{ansh}\t{tsh}\n')

    if 'deg_plan' in sdas_conf.keys():
        if in_files_num == 1:
            deg_result_dir,deg_shs = _deg(st_domain, sdas_conf, outdir)
            for domsh in domain_shs:
                for desh in deg_shs:
                    outshell.write(f'{domsh}\t{desh}\n')
        else:
            deg_result_dir,deg_shs = _deg(cell_anno, sdas_conf, outdir)
            for ansh in anno_shs:
                for desh in deg_shs:
                    outshell.write(f'{ansh}\t{desh}\n')
                    
        deg_enrich_sh = _degEnrich(deg_result_dir, sdas_conf, outdir)
        for desh in deg_shs:
            for esh in deg_enrich_sh:
                outshell.write(f'{desh}\t{esh}\n')

    if 'gsea_plan' in sdas_conf.keys():
        if in_files_num == 1:
            gsea_shs = _gsea(st_domain, sdas_conf, outdir)
            for domsh in domain_shs:
                for gseash in gsea_shs:
                    outshell.write(f'{domsh}\t{gseash}\n')
        else:
            gsea_shs = _gsea(cell_anno, sdas_conf, outdir)
            for ansh in anno_shs:
                for gseash in gsea_shs:
                    outshell.write(f'{ansh}\t{gseash}\n')

    if 'gsva_plan' in sdas_conf.keys():
        if in_files_num == 1:
            gsva_shs = _gsva(st_domain, sdas_conf, outdir)
            for domsh in domain_shs:
                for gsvash in gsva_shs:
                    outshell.write(f'{domsh}\t{gsvash}\n')
        else:
            gsva_shs = _gsva(cell_anno, sdas_conf, outdir)
            for ansh in anno_shs:
                for gsvash in gsva_shs:
                    outshell.write(f'{ansh}\t{gsvash}\n')

    outshell.close()

if __name__ == '__main__':
    main()
