#!/usr/bin/python
import os, sys, hashlib, shutil, traceback

PROFILE_FILE="profile.bin"
def main(mouse_sensi):
    profile_path=os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))+"/"
    print ("profile_path: %s!" % profile_path)
    # backup current profile in profile.bin.bak
    shutil.copyfile(profile_path+PROFILE_FILE, profile_path+PROFILE_FILE+".bak")
    
    # read profile.bin
    # update mouse sensi
    # recompute sha1
    # first 20 bytes are sha1 of the rest
    with open(profile_path+PROFILE_FILE, 'rb') as f:
        config=bytearray(f.read()[20:])
    
    # ================= CHANGE OFFSET HERE =====================
    # I used HxD as a hex editor, but Cheat Engine should also work
    # change below (current position is 10C)
    config[0x10C-20]=mouse_sensi
    # ==========================================================
    
    hash=hashlib.sha1()
    hash.update(config)
    print ("new profile hash %s : " % hash.hexdigest())
    config=bytearray(hash.digest())+config
    
    # rewrite profile.bin file
    with open(profile_path+PROFILE_FILE, 'wb') as f:
        f.write(config)
        
if __name__=='__main__':
    print ("Borderlands 2 mouse sensitivity updater")
    
    if len(sys.argv)>1:
        try:
            sensi=int(sys.argv[1])
            if sensi<0 or sensi>255:
                raise ValueError
            else:
                main(int(sys.argv[1]))
        except ValueError:
            print ("[-] Invalid value"      )
        except Exception as e:
            print (e)
    else:
        print ("Usage is %s <mouse sensi>")
        sys.exit()
