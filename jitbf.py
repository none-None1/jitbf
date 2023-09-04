"""
Brainfuck jit interpreter in Python
"""
try:
    import llvmlite.binding as llvm
except:
    raise ImportError('The package requires llvmlite, please install it via "pip install llvmlite"')
from ctypes import *
from uuid import uuid4
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()
engines=[]
def rndstr():
    return str(uuid4()).replace('-','_')
def fmt(code):
    rnds=[]
    for i in range(6):
        rnds.append('a'+rndstr())
        code=code.replace('$rnd.'+str(i),rnds[i])
    return code
def optfmt(code,times):
    rnds=[]
    for i in range(6):
        rnds.append('a'+rndstr())
        code=code.replace('$rnd.'+str(i),rnds[i])
    code = code.replace('$t',str(times))
    return code
def _bf2ll(bf,cellsize=300000):
    ll='''
declare i8 @getchar()
declare void @putchar(i8)
declare i8* @malloc(i32)
declare i8* @memset(i8*,i32,i32)
define i32 @main(){
    %arr=call i8* @malloc(i32 '''+str(cellsize)+''')
    call i8* @memset(i8* %arr, i32 0, i32 '''+str(cellsize)+''')
    %p=alloca i8*
    store i8* %arr, i8 **%p
'''
    opcodes={'+':'''
    %$rnd.0=load i8*,i8**%p
    %$rnd.1=load i8,i8*%$rnd.0
    %$rnd.2=add i8 %$rnd.1,1
    store i8 %$rnd.2,i8*%$rnd.0 
    ''','-':'''
    %$rnd.0=load i8*,i8**%p
    %$rnd.1=load i8,i8*%$rnd.0
    %$rnd.2=sub i8 %$rnd.1,1
    store i8 %$rnd.2,i8*%$rnd.0 
    ''','.':'''
    %$rnd.0=load i8*,i8**%p
    %$rnd.1=load i8,i8*%$rnd.0
    call void @putchar(i8 %$rnd.1)
    ''',',':'''
    %$rnd.0=load i8*,i8**%p
    %$rnd.1=call i8 @getchar()
    store i8 %$rnd.1,i8*%$rnd.0
    ''','>':'''
    %$rnd.0=load i8*,i8**%p
    %$rnd.1=ptrtoint i8* %$rnd.0 to i64
    %$rnd.2=add i64 %$rnd.1,1
    %$rnd.3=inttoptr i64 %$rnd.2 to i8*
    store i8* %$rnd.3,i8**%p
    ''','<':'''
    %$rnd.0=load i8*,i8**%p
    %$rnd.1=ptrtoint i8* %$rnd.0 to i64
    %$rnd.2=sub i64 %$rnd.1,1
    %$rnd.3=inttoptr i64 %$rnd.2 to i8*
    store i8* %$rnd.3,i8**%p
    '''
    }
    left_llcode='''
    %$rnd.0=load i8*,i8**%p
    %$rnd.1=load i8,i8*%$rnd.0
    %$rnd.2=icmp eq i8 %$rnd.1,0
    br i1 %$rnd.2, label %$2,label %$1
$1:
    '''
    right_llcode='''
    %$rnd.0=load i8*,i8**%p
    %$rnd.1=load i8,i8*%$rnd.0
    %$rnd.2=icmp eq i8 %$rnd.1,0
    br i1 %$rnd.2, label %$2,label %$1
$2:
    '''
    stack=[]
    matched={}
    labelcode={}
    for i,j in enumerate(bf):
        if j=='[':
            stack.append(i)
        if j==']':
            m=stack.pop()
            matched[m]=i
            matched[i]=m
            labelcode[m]='s'+rndstr()
            labelcode[i]='s'+rndstr()
    for j,i in enumerate(bf):
        if i not in '+-,.[]<>':
            continue
        if i not in '[]':
            try:
                ll+=fmt(opcodes[i])
            except:
                pass
        else:
            if i=='[':
                ll+=fmt(left_llcode.replace('$1',labelcode[j]).replace('$2',labelcode[matched[j]]))
            else:
                ll += fmt(right_llcode.replace('$2', labelcode[j]).replace('$1', labelcode[matched[j]]))
    ll+='''
    ret i32 0
}
    '''
    return ll
def optbf(bf):
    stack=[]
    for i in bf:
        if i not in '+-,.[]><':
            continue
        if i in '+-><' and stack and stack[-1][0]==i:
            stack[-1][1]+=1
        else:
            stack.append([i,1])
    return stack
def bf2ll_opt(bf,cellsize=300000):
    ll='''
declare i8 @getchar()
declare void @putchar(i8)
declare i8* @malloc(i32)
declare i8* @memset(i8*,i32,i32)
define i32 @main(){
    %arr=call i8* @malloc(i32 '''+str(cellsize)+''')
    call i8* @memset(i8* %arr, i32 0, i32 '''+str(cellsize)+''')
    %p=alloca i8*
    store i8* %arr, i8 **%p
'''
    opcodes={'+':'''
    %$rnd.0=load i8*,i8**%p
    %$rnd.1=load i8,i8*%$rnd.0
    %$rnd.2=add i8 %$rnd.1,$t
    store i8 %$rnd.2,i8*%$rnd.0 
    ''','-':'''
    %$rnd.0=load i8*,i8**%p
    %$rnd.1=load i8,i8*%$rnd.0
    %$rnd.2=sub i8 %$rnd.1,$t
    store i8 %$rnd.2,i8*%$rnd.0 
    ''','.':'''
    %$rnd.0=load i8*,i8**%p
    %$rnd.1=load i8,i8*%$rnd.0
    call void @putchar(i8 %$rnd.1)
    ''',',':'''
    %$rnd.0=load i8*,i8**%p
    %$rnd.1=call i8 @getchar()
    store i8 %$rnd.1,i8*%$rnd.0
    ''','>':'''
    %$rnd.0=load i8*,i8**%p
    %$rnd.1=ptrtoint i8* %$rnd.0 to i64
    %$rnd.2=add i64 %$rnd.1,$t
    %$rnd.3=inttoptr i64 %$rnd.2 to i8*
    store i8* %$rnd.3,i8**%p
    ''','<':'''
    %$rnd.0=load i8*,i8**%p
    %$rnd.1=ptrtoint i8* %$rnd.0 to i64
    %$rnd.2=sub i64 %$rnd.1,$t
    %$rnd.3=inttoptr i64 %$rnd.2 to i8*
    store i8* %$rnd.3,i8**%p
    '''
    }
    left_llcode='''
    %$rnd.0=load i8*,i8**%p
    %$rnd.1=load i8,i8*%$rnd.0
    %$rnd.2=icmp eq i8 %$rnd.1,0
    br i1 %$rnd.2, label %$2,label %$1
$1:
    '''
    right_llcode='''
    %$rnd.0=load i8*,i8**%p
    %$rnd.1=load i8,i8*%$rnd.0
    %$rnd.2=icmp eq i8 %$rnd.1,0
    br i1 %$rnd.2, label %$2,label %$1
$2:
    '''
    stack=[]
    matched={}
    labelcode={}
    for i,j in enumerate(bf):
        k=j[0]
        if k=='[':
            stack.append(i)
        if k==']':
            m=stack.pop()
            matched[m]=i
            matched[i]=m
            labelcode[m]='s'+rndstr()
            labelcode[i]='s'+rndstr()
    for j,i in enumerate(bf):
        k,l=i
        if k not in '+-,.[]<>':
            continue
        if k not in '[]':
            try:
                ll+=optfmt(opcodes[k],l)
            except:
                pass
        else:
            if k=='[':
                ll+=optfmt(left_llcode.replace('$1',labelcode[j]).replace('$2',labelcode[matched[j]]),l)
            else:
                ll += optfmt(right_llcode.replace('$2', labelcode[j]).replace('$1', labelcode[matched[j]]),l)
    ll+='''
    ret i32 0
}
    '''
    return ll
def ll2func(c0de):
    target=llvm.Target.from_default_triple()
    tm=target.create_target_machine()
    mod=llvm.parse_assembly('')
    e=llvm.create_mcjit_compiler(mod,tm)
    m=llvm.parse_assembly(c0de)
    m.verify()
    e.add_module(m)
    def f():
        func = e.get_function_address('main')
        cfunc = CFUNCTYPE(c_int32)(func)
        cfunc()
    return f
def bf2ll(bf,cellsize=300000,opt=True):
    if opt:
        return bf2ll_opt(optbf(bf),cellsize)
    else:
        return _bf2ll(bf,cellsize)
def bf2jit(bf,cellsize=300000,opt=True):
    """
    Creates a function which runs the brainfuck code you provided
    :param bf: Brainfuck code
    :return: A function which runs the brainfuck code you provided
    :param cellsize: Number of cells, default is 300000
    :param opt: Optimize or not, default is True
    """
    return ll2func(bf2ll(bf,cellsize,opt))
def _test():
    import sys
    if len(sys.argv)!=2 and len(sys.argv)!=3 and len(sys.argv)!=4:
        print('Usage: jitbf <filename> [<cellsize>] [-o]')
        return 1
    opt = False
    if '-o' in sys.argv:
        opt=True
        sys.argv.remove('-o')
    fn=sys.argv[1]
    cellsize=300000
    if len(sys.argv)==3:
        cellsize=int(sys.argv[2])
    with open(fn,'r',errors='ignore') as f:
        c0de=f.read()
    jit=bf2jit(c0de,cellsize,opt)
    jit()
__all__=['bf2jit']
if __name__=='__main__':
    _test()