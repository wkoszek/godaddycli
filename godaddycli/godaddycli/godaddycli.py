#!/usr/bin/env python
# Copyright 2015 by Wojciech A. Koszek <wojciech@koszek.com>
# -*- coding: utf-8 -*-

import os
import sys
import json
import argparse
import getpass
from pygodaddy import GoDaddyClient

g_dns_record_types = [ "A", "CNAME", "MX", "TXT", "SRV", "NS", "AAAA" ]
g_debug = False

def dbg(s):
    if g_debug != True:
        return
    print "# debug: " + str(s)

def parse_args(args):
    parser = argparse.ArgumentParser(description="GoDaddy.com CLI")
    parser.add_argument("--user")
    parser.add_argument("--password")
    parser.add_argument("--domain", action="append", default=None)
    parser.add_argument("--recordtype", action="append", default=None)
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument("--delete", action="append", default=None)
    parser.add_argument("--update", action="append", default=None)
    parser.add_argument("--list", action="store_true", default=True)
    parser.add_argument("--value", action="store", default=None)
    args = parser.parse_args(args)
    return args

def godaddycli_list(client, cfg):
    domains_cli = cfg.domain
    recordtypes_cli = cfg.recordtype

    dbg("passed from CLI:")
    dbg(domains_cli)
    dbg(recordtypes_cli)

    domains = client.find_domains()
    dbg(domains)

    if domains_cli is not None:
        for d_cli in domains_cli:
            if d_cli not in domains:
                print "Domain {0} not in GoDaddy!".format(d_cli)
                sys.exit(1)
        domains = domains_cli

    recordtypes = g_dns_record_types
    if recordtypes_cli is not None:
        for r in recordtypes_cli:
            if r not in recordtypes:
                print "Record type {0} is unknown!".format(r)
                sys.exit(1)
        recordtypes = recordtypes_cli

    dbg("to scan")
    dbg(domains)
    dbg(recordtypes)

    for domain_name in domains:
        for record_type in recordtypes:
            domain_data_all = client.find_dns_records(domain_name, record_type)
            for domain_data in domain_data_all:
                print domain_name, record_type, domain_data.hostname, domain_data.value

def godaddycli_delete(client, cfg):
    dbg("delete")
    for hostname in cfg.delete:
        dbg(hostname)
        client.delete_dns_record(hostname)
            # warning: pygodaddy only supports A type for deletion
    return 0

def godaddycli_update(client, cfg):
    dbg("update")
    recordtype = "A"
    if cfg.recordtype is not None:
        recordtype = cfg.recordtype[0]
    for hostname in cfg.update:
        dbg(hostname)
        client.update_dns_record(hostname, cfg.value, recordtype)
    return 0

def godaddycli(username, password, cfg):
    client = GoDaddyClient()
    c = client.login(username, password)
    if not c:
            print "couldn't login"
            sys.exit(1)

    if cfg.delete is not None:
        godaddycli_delete(client, cfg)
        return 0
    if cfg.update is not None:
        godaddycli_update(client, cfg)
        return 0
    if cfg.list is not None:
        godaddycli_list(client, cfg)
        return 0

def doit(cfg):
    global g_debug

    g_debug = cfg.debug
    home_dir = os.environ["HOME"]

    user = password = cfg_data = None
    cfg_filename = home_dir + "/.godaddyclirc"
    if os.path.isfile(cfg_filename):
        with open(cfg_filename, "r") as f:
            cfg_data = json.load(f)
        f.close()

        valid_fields_count = 0
        if "user" in cfg_data.keys():
            user = cfg_data["user"]
        if "password" in cfg_data.keys():
            password = cfg_data["password"]

    maybe_save = False

    if cfg.user:
        user = cfg.user
    if user is None:
        sys.stdout.write("Enter GoDaddy user    : ")
        user = sys.stdin.readline().strip("\n")
        maybe_save = True

    if cfg.password:
        password = cfg.password
    if password is None:
        password = getpass.getpass("Enter GoDaddy password: ")
        maybe_save = True

    dbg("user: " + user)
    dbg("pass: " + password)
    dbg("home: " + home_dir)

    will_save = False
    if maybe_save:
        sys.stdout.write("Do you want to save your password in " +
            cfg_filename + "? Enter 'yes' or 'no': ")
        while True:
            yes_or_no = sys.stdin.readline().strip("\n")
            if yes_or_no != "yes" and yes_or_no != "no":
                print "Only 'yes' or 'no' supported"
                continue
            if yes_or_no == "yes":
                will_save = True
            break

    if will_save:
        data_to_save = {
            "user"      : user,
            "password"  : password
        };
        with open(cfg_filename, "w") as f:
            js = json.dump(data_to_save, f)
        f.close()

    if cfg.update is not None and cfg.value is None:
        print "For --update you must specify --value too"
        sys.exit(1)

    return godaddycli(user, password, cfg)

def main():
    cfg = parse_args(sys.argv[1:])
    doit(cfg)

if __name__ == "__main__":
    sys.exit(main())
