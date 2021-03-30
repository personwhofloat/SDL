import yaml
class Config():
    def __init__(self):
        pass
    def merge_from_file(self, path):
        res = yaml.load(open(path,'r'), Loader=yaml.Loader)
        for k,v in res.items():
            setattr(self, k, v)
    def merge_from_args(self, args):
        for k,v in vars(args).items():
            setattr(self, k, v)
    
if __name__ == '__main__':
    cfg = Config()
    cfg.merge_from_file('doc.yaml')
    print(cfg.fontsize)