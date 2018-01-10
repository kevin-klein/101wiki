from django.db import models
from git import Repo
import git

import shutil
import os
import json

def abs_path(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', path))

env = {
    'config101': abs_path('../101worker/configs/production.json'),
    'config101schema': abs_path('../101worker/schemas/config.schema.json'),
    'data101url': 'http://data.101companies.org/',
    'diffs101dir': abs_path('../101diffs'),
    'dumps101dir': abs_path('../101web/data/dumps'),
    'data101dir': abs_path('../101web/data'),
    'endpoint101url': 'http://101companies.org/endpoint/',
    'explorer101url': 'http://101companies.org/resources/',
    'extractor101dir': abs_path('../101worker/extractors'),
    'gatheredGeshi101dir': abs_path('../101results/geshi'),
    'gitdeps101dir': abs_path('../101results/gitdeps'),
    'gitdeps101url': 'http://101companies.org/pullRepo.json',
    'last101run': '0',
    'logs101dir': abs_path('../101logs'),
    'module101schema': abs_path( '../101worker/schemas/module.schema.json'),
    'modules101dir': abs_path('../101worker/modules'),
    'ontoDir': abs_path('../101web/data/onto'),
    'output101dir': abs_path('..'),
    'predicates101deps': abs_path('../101worker/modules/predicates101meta/module.json'),
    'predicates101dir': abs_path('../101worker/predicates'),
    'repo101dir': abs_path('../101results/101repo'),
    'repo101url': 'https://github.com/101companies/101repo',
    'results101dir': abs_path('../101results'),
    'targets101dir': abs_path('../101web/data/resources'),
    'temps101dir': abs_path('../101temps'),
    'themes101dir': abs_path('../101web/data/resources/themes'),
    'validator101dir': abs_path('../101worker/validators'),
    'views101dir': abs_path('../101web/data/views'),
    'web101dir': abs_path('../101web'),
    'wiki101url': 'http://101companies.org/wiki/',
    'worker101dir': abs_path('../101worker')
}

def convert_diff(diff):
    file_1 = diff.a_path
    file_2 = diff.b_path

    if diff.a_mode == 0 and diff.a_blob is None:
        return { 'type': 'DELETED_FILE', 'file': file_2 }

    elif diff.b_mode == 0 and diff.b_blob is None:
        return { 'type': 'NEW_FILE', 'file': file_1 }

    else:
        return { 'type': 'FILE_CHANGED', 'file': file_1 }

def copy_gitdeps(changes, env):
    for change in changes:
        if change['type'] == 'NEW_FILE':
            target_file = os.path.join(env['repo101dir'], '/'.join(change['file'].split('/')[2:]))
            dirname = os.path.dirname(target_file)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            source_file = os.path.join(env['gitdeps101dir'], change['file'])

            shutil.copyfile(source_file, target_file)

def pull_gitdeps(env, gitdeps):
    def pull_gitdep(dep):
        user = dep['sourcerepo'].split('/')[-2]
        filename = dep['sourcerepo'].split('/')[-1].replace('.git', '')
        path = os.path.join(env['gitdeps101dir'], user, filename)
        if os.path.exists(os.path.join(path, '.git')):
            repo = Repo(path)
            return list(pull_repo(repo))
        else:
            try:
                print(dep['sourcerepo'])
                repo = Repo.clone_from(dep['sourcerepo'], path, branch='master')
                result = []
                for root, dirnames, filenames in os.walk(path):
                    for f in filenames:
                        f = os.path.join(root, f).replace(env['gitdeps101dir'], '')[1:]
                        if '.git/' in f:
                            continue
                        result.append({ 'type': 'NEW_FILE', 'file':  f})
                return result
            except git.exc.GitCommandError:
                return []

    return sum(list(map(pull_gitdep, gitdeps)), [])

def load_gitdeps(env):
    with open(os.path.abspath(os.path.join(env['repo101dir'], '.gitdeps'))) as f:
        return json.load(f)

def pull_repo(repo):
    base_commit = repo.head.commit.hexsha
    info = repo.remotes.origin.pull('master')[0]
    diffs = info.commit.diff(base_commit)
    return list(map(lambda diff: convert_diff(diff), diffs))

def create_repo(env):
    try:
        return Repo(env['repo101dir'])
    except git.exc.InvalidGitRepositoryError:
        return Repo.clone_from('https://github.com/101companies/101repo.git', env['repo101dir'], branch='master')

def checkout_commit(repo, commit):
    repo.git.checkout(commit)

def history(repo, commit):
    return repo.iter_commits(commit)
