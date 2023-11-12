window.pdocSearch = (function () {
    /** elasticlunr - http://weixsong.github.io * Copyright (C) 2017 Oliver Nightingale * Copyright (C) 2017 Wei Song * MIT Licensed */!function () {
        function e(e) {
            if (null === e || "object" != typeof e) return e;
            var t = e.constructor();
            for (var n in e) e.hasOwnProperty(n) && (t[n] = e[n]);
            return t
        }

        var t = function (e) {
            var n = new t.Index;
            return n.pipeline.add(t.trimmer, t.stopWordFilter, t.stemmer), e && e.call(n, n), n
        };
        t.version = "0.9.5", lunr = t, t.utils = {}, t.utils.warn = function (e) {
            return function (t) {
                e.console && console.warn && console.warn(t)
            }
        }(this), t.utils.toString = function (e) {
            return void 0 === e || null === e ? "" : e.toString()
        }, t.EventEmitter = function () {
            this.events = {}
        }, t.EventEmitter.prototype.addListener = function () {
            var e = Array.prototype.slice.call(arguments), t = e.pop(), n = e;
            if ("function" != typeof t) throw new TypeError("last argument must be a function");
            n.forEach(function (e) {
                this.hasHandler(e) || (this.events[e] = []), this.events[e].push(t)
            }, this)
        }, t.EventEmitter.prototype.removeListener = function (e, t) {
            if (this.hasHandler(e)) {
                var n = this.events[e].indexOf(t);
                -1 !== n && (this.events[e].splice(n, 1), 0 == this.events[e].length && delete this.events[e])
            }
        }, t.EventEmitter.prototype.emit = function (e) {
            if (this.hasHandler(e)) {
                var t = Array.prototype.slice.call(arguments, 1);
                this.events[e].forEach(function (e) {
                    e.apply(void 0, t)
                }, this)
            }
        }, t.EventEmitter.prototype.hasHandler = function (e) {
            return e in this.events
        }, t.tokenizer = function (e) {
            if (!arguments.length || null === e || void 0 === e) return [];
            if (Array.isArray(e)) {
                var n = e.filter(function (e) {
                    return null === e || void 0 === e ? !1 : !0
                });
                n = n.map(function (e) {
                    return t.utils.toString(e).toLowerCase()
                });
                var i = [];
                return n.forEach(function (e) {
                    var n = e.split(t.tokenizer.seperator);
                    i = i.concat(n)
                }, this), i
            }
            return e.toString().trim().toLowerCase().split(t.tokenizer.seperator)
        }, t.tokenizer.defaultSeperator = /[\s\-]+/, t.tokenizer.seperator = t.tokenizer.defaultSeperator, t.tokenizer.setSeperator = function (e) {
            null !== e && void 0 !== e && "object" == typeof e && (t.tokenizer.seperator = e)
        }, t.tokenizer.resetSeperator = function () {
            t.tokenizer.seperator = t.tokenizer.defaultSeperator
        }, t.tokenizer.getSeperator = function () {
            return t.tokenizer.seperator
        }, t.Pipeline = function () {
            this._queue = []
        }, t.Pipeline.registeredFunctions = {}, t.Pipeline.registerFunction = function (e, n) {
            n in t.Pipeline.registeredFunctions && t.utils.warn("Overwriting existing registered function: " + n), e.label = n, t.Pipeline.registeredFunctions[n] = e
        }, t.Pipeline.getRegisteredFunction = function (e) {
            return e in t.Pipeline.registeredFunctions != !0 ? null : t.Pipeline.registeredFunctions[e]
        }, t.Pipeline.warnIfFunctionNotRegistered = function (e) {
            var n = e.label && e.label in this.registeredFunctions;
            n || t.utils.warn("Function is not registered with pipeline. This may cause problems when serialising the index.\n", e)
        }, t.Pipeline.load = function (e) {
            var n = new t.Pipeline;
            return e.forEach(function (e) {
                var i = t.Pipeline.getRegisteredFunction(e);
                if (!i) throw new Error("Cannot load un-registered function: " + e);
                n.add(i)
            }), n
        }, t.Pipeline.prototype.add = function () {
            var e = Array.prototype.slice.call(arguments);
            e.forEach(function (e) {
                t.Pipeline.warnIfFunctionNotRegistered(e), this._queue.push(e)
            }, this)
        }, t.Pipeline.prototype.after = function (e, n) {
            t.Pipeline.warnIfFunctionNotRegistered(n);
            var i = this._queue.indexOf(e);
            if (-1 === i) throw new Error("Cannot find existingFn");
            this._queue.splice(i + 1, 0, n)
        }, t.Pipeline.prototype.before = function (e, n) {
            t.Pipeline.warnIfFunctionNotRegistered(n);
            var i = this._queue.indexOf(e);
            if (-1 === i) throw new Error("Cannot find existingFn");
            this._queue.splice(i, 0, n)
        }, t.Pipeline.prototype.remove = function (e) {
            var t = this._queue.indexOf(e);
            -1 !== t && this._queue.splice(t, 1)
        }, t.Pipeline.prototype.run = function (e) {
            for (var t = [], n = e.length, i = this._queue.length, o = 0; n > o; o++) {
                for (var r = e[o], s = 0; i > s && (r = this._queue[s](r, o, e), void 0 !== r && null !== r); s++) ;
                void 0 !== r && null !== r && t.push(r)
            }
            return t
        }, t.Pipeline.prototype.reset = function () {
            this._queue = []
        }, t.Pipeline.prototype.get = function () {
            return this._queue
        }, t.Pipeline.prototype.toJSON = function () {
            return this._queue.map(function (e) {
                return t.Pipeline.warnIfFunctionNotRegistered(e), e.label
            })
        }, t.Index = function () {
            this._fields = [], this._ref = "id", this.pipeline = new t.Pipeline, this.documentStore = new t.DocumentStore, this.index = {}, this.eventEmitter = new t.EventEmitter, this._idfCache = {}, this.on("add", "remove", "update", function () {
                this._idfCache = {}
            }.bind(this))
        }, t.Index.prototype.on = function () {
            var e = Array.prototype.slice.call(arguments);
            return this.eventEmitter.addListener.apply(this.eventEmitter, e)
        }, t.Index.prototype.off = function (e, t) {
            return this.eventEmitter.removeListener(e, t)
        }, t.Index.load = function (e) {
            e.version !== t.version && t.utils.warn("version mismatch: current " + t.version + " importing " + e.version);
            var n = new this;
            n._fields = e.fields, n._ref = e.ref, n.documentStore = t.DocumentStore.load(e.documentStore), n.pipeline = t.Pipeline.load(e.pipeline), n.index = {};
            for (var i in e.index) n.index[i] = t.InvertedIndex.load(e.index[i]);
            return n
        }, t.Index.prototype.addField = function (e) {
            return this._fields.push(e), this.index[e] = new t.InvertedIndex, this
        }, t.Index.prototype.setRef = function (e) {
            return this._ref = e, this
        }, t.Index.prototype.saveDocument = function (e) {
            return this.documentStore = new t.DocumentStore(e), this
        }, t.Index.prototype.addDoc = function (e, n) {
            if (e) {
                var n = void 0 === n ? !0 : n, i = e[this._ref];
                this.documentStore.addDoc(i, e), this._fields.forEach(function (n) {
                    var o = this.pipeline.run(t.tokenizer(e[n]));
                    this.documentStore.addFieldLength(i, n, o.length);
                    var r = {};
                    o.forEach(function (e) {
                        e in r ? r[e] += 1 : r[e] = 1
                    }, this);
                    for (var s in r) {
                        var u = r[s];
                        u = Math.sqrt(u), this.index[n].addToken(s, {ref: i, tf: u})
                    }
                }, this), n && this.eventEmitter.emit("add", e, this)
            }
        }, t.Index.prototype.removeDocByRef = function (e) {
            if (e && this.documentStore.isDocStored() !== !1 && this.documentStore.hasDoc(e)) {
                var t = this.documentStore.getDoc(e);
                this.removeDoc(t, !1)
            }
        }, t.Index.prototype.removeDoc = function (e, n) {
            if (e) {
                var n = void 0 === n ? !0 : n, i = e[this._ref];
                this.documentStore.hasDoc(i) && (this.documentStore.removeDoc(i), this._fields.forEach(function (n) {
                    var o = this.pipeline.run(t.tokenizer(e[n]));
                    o.forEach(function (e) {
                        this.index[n].removeToken(e, i)
                    }, this)
                }, this), n && this.eventEmitter.emit("remove", e, this))
            }
        }, t.Index.prototype.updateDoc = function (e, t) {
            var t = void 0 === t ? !0 : t;
            this.removeDocByRef(e[this._ref], !1), this.addDoc(e, !1), t && this.eventEmitter.emit("update", e, this)
        }, t.Index.prototype.idf = function (e, t) {
            var n = "@" + t + "/" + e;
            if (Object.prototype.hasOwnProperty.call(this._idfCache, n)) return this._idfCache[n];
            var i = this.index[t].getDocFreq(e), o = 1 + Math.log(this.documentStore.length / (i + 1));
            return this._idfCache[n] = o, o
        }, t.Index.prototype.getFields = function () {
            return this._fields.slice()
        }, t.Index.prototype.search = function (e, n) {
            if (!e) return [];
            e = "string" == typeof e ? {any: e} : JSON.parse(JSON.stringify(e));
            var i = null;
            null != n && (i = JSON.stringify(n));
            for (var o = new t.Configuration(i, this.getFields()).get(), r = {}, s = Object.keys(e), u = 0; u < s.length; u++) {
                var a = s[u];
                r[a] = this.pipeline.run(t.tokenizer(e[a]))
            }
            var l = {};
            for (var c in o) {
                var d = r[c] || r.any;
                if (d) {
                    var f = this.fieldSearch(d, c, o), h = o[c].boost;
                    for (var p in f) f[p] = f[p] * h;
                    for (var p in f) p in l ? l[p] += f[p] : l[p] = f[p]
                }
            }
            var v, g = [];
            for (var p in l) v = {
                ref: p,
                score: l[p]
            }, this.documentStore.hasDoc(p) && (v.doc = this.documentStore.getDoc(p)), g.push(v);
            return g.sort(function (e, t) {
                return t.score - e.score
            }), g
        }, t.Index.prototype.fieldSearch = function (e, t, n) {
            var i = n[t].bool, o = n[t].expand, r = n[t].boost, s = null, u = {};
            return 0 !== r ? (e.forEach(function (e) {
                var n = [e];
                1 == o && (n = this.index[t].expandToken(e));
                var r = {};
                n.forEach(function (n) {
                    var o = this.index[t].getDocs(n), a = this.idf(n, t);
                    if (s && "AND" == i) {
                        var l = {};
                        for (var c in s) c in o && (l[c] = o[c]);
                        o = l
                    }
                    n == e && this.fieldSearchStats(u, n, o);
                    for (var c in o) {
                        var d = this.index[t].getTermFrequency(n, c), f = this.documentStore.getFieldLength(c, t),
                            h = 1;
                        0 != f && (h = 1 / Math.sqrt(f));
                        var p = 1;
                        n != e && (p = .15 * (1 - (n.length - e.length) / n.length));
                        var v = d * a * h * p;
                        c in r ? r[c] += v : r[c] = v
                    }
                }, this), s = this.mergeScores(s, r, i)
            }, this), s = this.coordNorm(s, u, e.length)) : void 0
        }, t.Index.prototype.mergeScores = function (e, t, n) {
            if (!e) return t;
            if ("AND" == n) {
                var i = {};
                for (var o in t) o in e && (i[o] = e[o] + t[o]);
                return i
            }
            for (var o in t) o in e ? e[o] += t[o] : e[o] = t[o];
            return e
        }, t.Index.prototype.fieldSearchStats = function (e, t, n) {
            for (var i in n) i in e ? e[i].push(t) : e[i] = [t]
        }, t.Index.prototype.coordNorm = function (e, t, n) {
            for (var i in e) if (i in t) {
                var o = t[i].length;
                e[i] = e[i] * o / n
            }
            return e
        }, t.Index.prototype.toJSON = function () {
            var e = {};
            return this._fields.forEach(function (t) {
                e[t] = this.index[t].toJSON()
            }, this), {
                version: t.version,
                fields: this._fields,
                ref: this._ref,
                documentStore: this.documentStore.toJSON(),
                index: e,
                pipeline: this.pipeline.toJSON()
            }
        }, t.Index.prototype.use = function (e) {
            var t = Array.prototype.slice.call(arguments, 1);
            t.unshift(this), e.apply(this, t)
        }, t.DocumentStore = function (e) {
            this._save = null === e || void 0 === e ? !0 : e, this.docs = {}, this.docInfo = {}, this.length = 0
        }, t.DocumentStore.load = function (e) {
            var t = new this;
            return t.length = e.length, t.docs = e.docs, t.docInfo = e.docInfo, t._save = e.save, t
        }, t.DocumentStore.prototype.isDocStored = function () {
            return this._save
        }, t.DocumentStore.prototype.addDoc = function (t, n) {
            this.hasDoc(t) || this.length++, this.docs[t] = this._save === !0 ? e(n) : null
        }, t.DocumentStore.prototype.getDoc = function (e) {
            return this.hasDoc(e) === !1 ? null : this.docs[e]
        }, t.DocumentStore.prototype.hasDoc = function (e) {
            return e in this.docs
        }, t.DocumentStore.prototype.removeDoc = function (e) {
            this.hasDoc(e) && (delete this.docs[e], delete this.docInfo[e], this.length--)
        }, t.DocumentStore.prototype.addFieldLength = function (e, t, n) {
            null !== e && void 0 !== e && 0 != this.hasDoc(e) && (this.docInfo[e] || (this.docInfo[e] = {}), this.docInfo[e][t] = n)
        }, t.DocumentStore.prototype.updateFieldLength = function (e, t, n) {
            null !== e && void 0 !== e && 0 != this.hasDoc(e) && this.addFieldLength(e, t, n)
        }, t.DocumentStore.prototype.getFieldLength = function (e, t) {
            return null === e || void 0 === e ? 0 : e in this.docs && t in this.docInfo[e] ? this.docInfo[e][t] : 0
        }, t.DocumentStore.prototype.toJSON = function () {
            return {docs: this.docs, docInfo: this.docInfo, length: this.length, save: this._save}
        }, t.stemmer = function () {
            var e = {
                    ational: "ate",
                    tional: "tion",
                    enci: "ence",
                    anci: "ance",
                    izer: "ize",
                    bli: "ble",
                    alli: "al",
                    entli: "ent",
                    eli: "e",
                    ousli: "ous",
                    ization: "ize",
                    ation: "ate",
                    ator: "ate",
                    alism: "al",
                    iveness: "ive",
                    fulness: "ful",
                    ousness: "ous",
                    aliti: "al",
                    iviti: "ive",
                    biliti: "ble",
                    logi: "log"
                }, t = {icate: "ic", ative: "", alize: "al", iciti: "ic", ical: "ic", ful: "", ness: ""}, n = "[^aeiou]",
                i = "[aeiouy]", o = n + "[^aeiouy]*", r = i + "[aeiou]*", s = "^(" + o + ")?" + r + o,
                u = "^(" + o + ")?" + r + o + "(" + r + ")?$", a = "^(" + o + ")?" + r + o + r + o,
                l = "^(" + o + ")?" + i, c = new RegExp(s), d = new RegExp(a), f = new RegExp(u), h = new RegExp(l),
                p = /^(.+?)(ss|i)es$/, v = /^(.+?)([^s])s$/, g = /^(.+?)eed$/, m = /^(.+?)(ed|ing)$/, y = /.$/,
                S = /(at|bl|iz)$/, x = new RegExp("([^aeiouylsz])\\1$"), w = new RegExp("^" + o + i + "[^aeiouwxy]$"),
                I = /^(.+?[^aeiou])y$/,
                b = /^(.+?)(ational|tional|enci|anci|izer|bli|alli|entli|eli|ousli|ization|ation|ator|alism|iveness|fulness|ousness|aliti|iviti|biliti|logi)$/,
                E = /^(.+?)(icate|ative|alize|iciti|ical|ful|ness)$/,
                D = /^(.+?)(al|ance|ence|er|ic|able|ible|ant|ement|ment|ent|ou|ism|ate|iti|ous|ive|ize)$/,
                F = /^(.+?)(s|t)(ion)$/, _ = /^(.+?)e$/, P = /ll$/, k = new RegExp("^" + o + i + "[^aeiouwxy]$"),
                z = function (n) {
                    var i, o, r, s, u, a, l;
                    if (n.length < 3) return n;
                    if (r = n.substr(0, 1), "y" == r && (n = r.toUpperCase() + n.substr(1)), s = p, u = v, s.test(n) ? n = n.replace(s, "$1$2") : u.test(n) && (n = n.replace(u, "$1$2")), s = g, u = m, s.test(n)) {
                        var z = s.exec(n);
                        s = c, s.test(z[1]) && (s = y, n = n.replace(s, ""))
                    } else if (u.test(n)) {
                        var z = u.exec(n);
                        i = z[1], u = h, u.test(i) && (n = i, u = S, a = x, l = w, u.test(n) ? n += "e" : a.test(n) ? (s = y, n = n.replace(s, "")) : l.test(n) && (n += "e"))
                    }
                    if (s = I, s.test(n)) {
                        var z = s.exec(n);
                        i = z[1], n = i + "i"
                    }
                    if (s = b, s.test(n)) {
                        var z = s.exec(n);
                        i = z[1], o = z[2], s = c, s.test(i) && (n = i + e[o])
                    }
                    if (s = E, s.test(n)) {
                        var z = s.exec(n);
                        i = z[1], o = z[2], s = c, s.test(i) && (n = i + t[o])
                    }
                    if (s = D, u = F, s.test(n)) {
                        var z = s.exec(n);
                        i = z[1], s = d, s.test(i) && (n = i)
                    } else if (u.test(n)) {
                        var z = u.exec(n);
                        i = z[1] + z[2], u = d, u.test(i) && (n = i)
                    }
                    if (s = _, s.test(n)) {
                        var z = s.exec(n);
                        i = z[1], s = d, u = f, a = k, (s.test(i) || u.test(i) && !a.test(i)) && (n = i)
                    }
                    return s = P, u = d, s.test(n) && u.test(n) && (s = y, n = n.replace(s, "")), "y" == r && (n = r.toLowerCase() + n.substr(1)), n
                };
            return z
        }(), t.Pipeline.registerFunction(t.stemmer, "stemmer"), t.stopWordFilter = function (e) {
            return e && t.stopWordFilter.stopWords[e] !== !0 ? e : void 0
        }, t.clearStopWords = function () {
            t.stopWordFilter.stopWords = {}
        }, t.addStopWords = function (e) {
            null != e && Array.isArray(e) !== !1 && e.forEach(function (e) {
                t.stopWordFilter.stopWords[e] = !0
            }, this)
        }, t.resetStopWords = function () {
            t.stopWordFilter.stopWords = t.defaultStopWords
        }, t.defaultStopWords = {
            "": !0,
            a: !0,
            able: !0,
            about: !0,
            across: !0,
            after: !0,
            all: !0,
            almost: !0,
            also: !0,
            am: !0,
            among: !0,
            an: !0,
            and: !0,
            any: !0,
            are: !0,
            as: !0,
            at: !0,
            be: !0,
            because: !0,
            been: !0,
            but: !0,
            by: !0,
            can: !0,
            cannot: !0,
            could: !0,
            dear: !0,
            did: !0,
            "do": !0,
            does: !0,
            either: !0,
            "else": !0,
            ever: !0,
            every: !0,
            "for": !0,
            from: !0,
            get: !0,
            got: !0,
            had: !0,
            has: !0,
            have: !0,
            he: !0,
            her: !0,
            hers: !0,
            him: !0,
            his: !0,
            how: !0,
            however: !0,
            i: !0,
            "if": !0,
            "in": !0,
            into: !0,
            is: !0,
            it: !0,
            its: !0,
            just: !0,
            least: !0,
            let: !0,
            like: !0,
            likely: !0,
            may: !0,
            me: !0,
            might: !0,
            most: !0,
            must: !0,
            my: !0,
            neither: !0,
            no: !0,
            nor: !0,
            not: !0,
            of: !0,
            off: !0,
            often: !0,
            on: !0,
            only: !0,
            or: !0,
            other: !0,
            our: !0,
            own: !0,
            rather: !0,
            said: !0,
            say: !0,
            says: !0,
            she: !0,
            should: !0,
            since: !0,
            so: !0,
            some: !0,
            than: !0,
            that: !0,
            the: !0,
            their: !0,
            them: !0,
            then: !0,
            there: !0,
            these: !0,
            they: !0,
            "this": !0,
            tis: !0,
            to: !0,
            too: !0,
            twas: !0,
            us: !0,
            wants: !0,
            was: !0,
            we: !0,
            were: !0,
            what: !0,
            when: !0,
            where: !0,
            which: !0,
            "while": !0,
            who: !0,
            whom: !0,
            why: !0,
            will: !0,
            "with": !0,
            would: !0,
            yet: !0,
            you: !0,
            your: !0
        }, t.stopWordFilter.stopWords = t.defaultStopWords, t.Pipeline.registerFunction(t.stopWordFilter, "stopWordFilter"), t.trimmer = function (e) {
            if (null === e || void 0 === e) throw new Error("token should not be undefined");
            return e.replace(/^\W+/, "").replace(/\W+$/, "")
        }, t.Pipeline.registerFunction(t.trimmer, "trimmer"), t.InvertedIndex = function () {
            this.root = {docs: {}, df: 0}
        }, t.InvertedIndex.load = function (e) {
            var t = new this;
            return t.root = e.root, t
        }, t.InvertedIndex.prototype.addToken = function (e, t, n) {
            for (var n = n || this.root, i = 0; i <= e.length - 1;) {
                var o = e[i];
                o in n || (n[o] = {docs: {}, df: 0}), i += 1, n = n[o]
            }
            var r = t.ref;
            n.docs[r] ? n.docs[r] = {tf: t.tf} : (n.docs[r] = {tf: t.tf}, n.df += 1)
        }, t.InvertedIndex.prototype.hasToken = function (e) {
            if (!e) return !1;
            for (var t = this.root, n = 0; n < e.length; n++) {
                if (!t[e[n]]) return !1;
                t = t[e[n]]
            }
            return !0
        }, t.InvertedIndex.prototype.getNode = function (e) {
            if (!e) return null;
            for (var t = this.root, n = 0; n < e.length; n++) {
                if (!t[e[n]]) return null;
                t = t[e[n]]
            }
            return t
        }, t.InvertedIndex.prototype.getDocs = function (e) {
            var t = this.getNode(e);
            return null == t ? {} : t.docs
        }, t.InvertedIndex.prototype.getTermFrequency = function (e, t) {
            var n = this.getNode(e);
            return null == n ? 0 : t in n.docs ? n.docs[t].tf : 0
        }, t.InvertedIndex.prototype.getDocFreq = function (e) {
            var t = this.getNode(e);
            return null == t ? 0 : t.df
        }, t.InvertedIndex.prototype.removeToken = function (e, t) {
            if (e) {
                var n = this.getNode(e);
                null != n && t in n.docs && (delete n.docs[t], n.df -= 1)
            }
        }, t.InvertedIndex.prototype.expandToken = function (e, t, n) {
            if (null == e || "" == e) return [];
            var t = t || [];
            if (void 0 == n && (n = this.getNode(e), null == n)) return t;
            n.df > 0 && t.push(e);
            for (var i in n) "docs" !== i && "df" !== i && this.expandToken(e + i, t, n[i]);
            return t
        }, t.InvertedIndex.prototype.toJSON = function () {
            return {root: this.root}
        }, t.Configuration = function (e, n) {
            var e = e || "";
            if (void 0 == n || null == n) throw new Error("fields should not be null");
            this.config = {};
            var i;
            try {
                i = JSON.parse(e), this.buildUserConfig(i, n)
            } catch (o) {
                t.utils.warn("user configuration parse failed, will use default configuration"), this.buildDefaultConfig(n)
            }
        }, t.Configuration.prototype.buildDefaultConfig = function (e) {
            this.reset(), e.forEach(function (e) {
                this.config[e] = {boost: 1, bool: "OR", expand: !1}
            }, this)
        }, t.Configuration.prototype.buildUserConfig = function (e, n) {
            var i = "OR", o = !1;
            if (this.reset(), "bool" in e && (i = e.bool || i), "expand" in e && (o = e.expand || o), "fields" in e) for (var r in e.fields) if (n.indexOf(r) > -1) {
                var s = e.fields[r], u = o;
                void 0 != s.expand && (u = s.expand), this.config[r] = {
                    boost: s.boost || 0 === s.boost ? s.boost : 1,
                    bool: s.bool || i,
                    expand: u
                }
            } else t.utils.warn("field name in user configuration not found in index instance fields"); else this.addAllFields2UserConfig(i, o, n)
        }, t.Configuration.prototype.addAllFields2UserConfig = function (e, t, n) {
            n.forEach(function (n) {
                this.config[n] = {boost: 1, bool: e, expand: t}
            }, this)
        }, t.Configuration.prototype.get = function () {
            return this.config
        }, t.Configuration.prototype.reset = function () {
            this.config = {}
        }, lunr.SortedSet = function () {
            this.length = 0, this.elements = []
        }, lunr.SortedSet.load = function (e) {
            var t = new this;
            return t.elements = e, t.length = e.length, t
        }, lunr.SortedSet.prototype.add = function () {
            var e, t;
            for (e = 0; e < arguments.length; e++) t = arguments[e], ~this.indexOf(t) || this.elements.splice(this.locationFor(t), 0, t);
            this.length = this.elements.length
        }, lunr.SortedSet.prototype.toArray = function () {
            return this.elements.slice()
        }, lunr.SortedSet.prototype.map = function (e, t) {
            return this.elements.map(e, t)
        }, lunr.SortedSet.prototype.forEach = function (e, t) {
            return this.elements.forEach(e, t)
        }, lunr.SortedSet.prototype.indexOf = function (e) {
            for (var t = 0, n = this.elements.length, i = n - t, o = t + Math.floor(i / 2), r = this.elements[o]; i > 1;) {
                if (r === e) return o;
                e > r && (t = o), r > e && (n = o), i = n - t, o = t + Math.floor(i / 2), r = this.elements[o]
            }
            return r === e ? o : -1
        }, lunr.SortedSet.prototype.locationFor = function (e) {
            for (var t = 0, n = this.elements.length, i = n - t, o = t + Math.floor(i / 2), r = this.elements[o]; i > 1;) e > r && (t = o), r > e && (n = o), i = n - t, o = t + Math.floor(i / 2), r = this.elements[o];
            return r > e ? o : e > r ? o + 1 : void 0
        }, lunr.SortedSet.prototype.intersect = function (e) {
            for (var t = new lunr.SortedSet, n = 0, i = 0, o = this.length, r = e.length, s = this.elements, u = e.elements; ;) {
                if (n > o - 1 || i > r - 1) break;
                s[n] !== u[i] ? s[n] < u[i] ? n++ : s[n] > u[i] && i++ : (t.add(s[n]), n++, i++)
            }
            return t
        }, lunr.SortedSet.prototype.clone = function () {
            var e = new lunr.SortedSet;
            return e.elements = this.toArray(), e.length = e.elements.length, e
        }, lunr.SortedSet.prototype.union = function (e) {
            var t, n, i;
            this.length >= e.length ? (t = this, n = e) : (t = e, n = this), i = t.clone();
            for (var o = 0, r = n.toArray(); o < r.length; o++) i.add(r[o]);
            return i
        }, lunr.SortedSet.prototype.toJSON = function () {
            return this.toArray()
        },function (e, t) {
            "function" == typeof define && define.amd ? define(t) : "object" == typeof exports ? module.exports = t() : e.elasticlunr = t()
        }(this, function () {
            return t
        })
    }();
    /** pdoc search index */const docs = [{
        "fullname": "open_precision",
        "modulename": "open_precision",
        "kind": "module",
        "doc": "<p>.. include: ../README.md</p>\n"
    }, {
        "fullname": "open_precision.api",
        "modulename": "open_precision.api",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.api.API",
        "modulename": "open_precision.api",
        "qualname": "API",
        "kind": "class",
        "doc": "<p>responsible for initializing and starting the (not really REST-ful) API</p>\n"
    }, {
        "fullname": "open_precision.api.API.__init__",
        "modulename": "open_precision.api",
        "qualname": "API.__init__",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">hub</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">system_hub</span><span class=\"o\">.</span><span class=\"n\">SystemHub</span></span>)</span>"
    }, {
        "fullname": "open_precision.api.API.queue_task",
        "modulename": "open_precision.api",
        "qualname": "API.queue_task",
        "kind": "variable",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.api.app",
        "modulename": "open_precision.api.app",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.api.app.url",
        "modulename": "open_precision.api.app",
        "qualname": "url",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&#x27;redis://redis:6379&#x27;"
    }, {
        "fullname": "open_precision.api.app.app",
        "modulename": "open_precision.api.app",
        "qualname": "app",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;fastapi.applications.FastAPI object&gt;"
    }, {
        "fullname": "open_precision.api.app.origins",
        "modulename": "open_precision.api.app",
        "qualname": "origins",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "[&#x27;*&#x27;]"
    }, {
        "fullname": "open_precision.api.app.root_router",
        "modulename": "open_precision.api.app",
        "qualname": "root_router",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;fastapi.routing.APIRouter object&gt;"
    }, {
        "fullname": "open_precision.api.app.root",
        "modulename": "open_precision.api.app",
        "qualname": "root",
        "kind": "function",
        "doc": "<p>Redirects to the frontend</p>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>RedirectResponse</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.app.api_router",
        "modulename": "open_precision.api.app",
        "qualname": "api_router",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;fastapi.routing.APIRouter object&gt;"
    }, {
        "fullname": "open_precision.api.app.origin_url",
        "modulename": "open_precision.api.app",
        "qualname": "origin_url",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": str | None",
        "default_value": "None"
    }, {
        "fullname": "open_precision.api.app.connect",
        "modulename": "open_precision.api.app",
        "qualname": "connect",
        "kind": "function",
        "doc": "<p>This func is called by the socketio server when a new client connects.\nIt will trigger an endpoint to trigger the corresponding inner function in the update loop.\nThis complex workaround is necessary, because the socketio server is not part of the fastapi app (it is just mounted\nto the path), so it cannot access the FastAPI's dependency to the system task queue function to trigger logic within\nthe update loop.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>sid</strong>:  socket id</li>\n<li><strong>environment</strong>:  environment dict</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">sid</span>, </span><span class=\"param\"><span class=\"n\">environment</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.app.disconnect",
        "modulename": "open_precision.api.app",
        "qualname": "disconnect",
        "kind": "function",
        "doc": "<p>This func is called by the socketio server when a client disconnects.\nIt will trigger an endpoint to trigger the corresponding inner function in the update loop.\nThis complex workaround is necessary, because the socketio server is not part of the fastapi app (it is just mounted\nto the path), so it cannot access the FastAPI's dependency to the system task queue function to trigger logic within\nthe update loop.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>sid</strong>:  socket id</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">sid</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.dependencies",
        "modulename": "open_precision.api.dependencies",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.api.dependencies.queue_system_task_dependency",
        "modulename": "open_precision.api.dependencies",
        "qualname": "queue_system_task_dependency",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.utils",
        "modulename": "open_precision.api.utils",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.api.utils.engine_endpoint",
        "modulename": "open_precision.api.utils",
        "qualname": "engine_endpoint",
        "kind": "function",
        "doc": "<p>Decorator to make fastapi endpoint functions from functions that need to be run in the engine (update loop in the\nmain thread).</p>\n\n<p>The decorated function must have a variable of type SystemHub as their first positional argument.\nThe following arguments can be treated as if the function was a FastAPI endpoint function, however it must still be\ndecorated as such!\nThe Endpoint will return the value returned by the decorated function as JSON (Attention: if it is a string, it will\nnot be JSONEncoded to allow for custom Encoders to be used within the wrapped function!). The status code of the\nreturned JSON will either be 200 (default), or 500 (if an error occured while executing the function).</p>\n\n<p>Usage:</p>\n\n<div class=\"pdoc-code codehilite\">\n<pre><span></span><code><span class=\"nd\">@app</span><span class=\"o\">.</span><span class=\"n\">post</span><span class=\"p\">(</span><span class=\"s2\">&quot;/generate</span><span class=\"si\">{foo}</span><span class=\"s2\">&quot;</span><span class=\"p\">)</span>\n<span class=\"nd\">@engine_endpoint</span>\n<span class=\"k\">def</span> <span class=\"nf\">_generate_course</span><span class=\"p\">(</span><span class=\"n\">hub</span><span class=\"p\">:</span> <span class=\"n\">SystemHub</span><span class=\"p\">,</span> <span class=\"n\">foo</span><span class=\"p\">:</span> <span class=\"nb\">str</span><span class=\"p\">,</span> <span class=\"n\">bar</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">=</span> <span class=\"s2\">&quot;b&quot;</span><span class=\"p\">,</span> <span class=\"n\">my_dependency</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">my_dep</span><span class=\"p\">)):</span>\n    <span class=\"n\">hub</span><span class=\"o\">.</span><span class=\"n\">plugins</span><span class=\"p\">[</span><span class=\"n\">Navigator</span><span class=\"p\">]</span><span class=\"o\">.</span><span class=\"n\">set_course_from_course_generator</span><span class=\"p\">()</span>\n    <span class=\"nb\">print</span><span class=\"p\">(</span><span class=\"n\">foo</span><span class=\"p\">,</span> <span class=\"n\">bar</span><span class=\"p\">)</span>\n    <span class=\"k\">return</span> <span class=\"n\">hub</span><span class=\"o\">.</span><span class=\"n\">plugins</span><span class=\"p\">[</span><span class=\"n\">Navigator</span><span class=\"p\">]</span><span class=\"o\">.</span><span class=\"n\">course</span>\n\n<span class=\"n\">Engine</span> <span class=\"n\">endpoint</span> <span class=\"n\">requests</span>  <span class=\"n\">can</span> <span class=\"n\">also</span> <span class=\"n\">be</span> <span class=\"n\">subscribed</span> <span class=\"n\">to</span><span class=\"o\">.</span> <span class=\"n\">This</span> <span class=\"n\">means</span> <span class=\"n\">that</span> <span class=\"n\">the</span> <span class=\"n\">endpoint</span> <span class=\"n\">will</span> <span class=\"n\">be</span> <span class=\"n\">called</span> <span class=\"n\">periodically</span> <span class=\"ow\">and</span>\n<span class=\"n\">the</span> <span class=\"n\">returned</span> <span class=\"n\">value</span> <span class=\"n\">will</span> <span class=\"n\">be</span> <span class=\"n\">sent</span> <span class=\"n\">to</span> <span class=\"n\">the</span> <span class=\"n\">client</span> <span class=\"n\">via</span> <span class=\"n\">socketio</span><span class=\"o\">.</span> <span class=\"n\">To</span> <span class=\"n\">subscribe</span> <span class=\"n\">to</span> <span class=\"n\">an</span> <span class=\"n\">endpoint</span><span class=\"p\">,</span> <span class=\"n\">the</span> <span class=\"n\">client</span> <span class=\"n\">must</span> <span class=\"n\">send</span> <span class=\"n\">the</span>\n<span class=\"n\">request</span> <span class=\"n\">that</span> <span class=\"n\">should</span> <span class=\"n\">be</span> <span class=\"n\">subscribed</span> <span class=\"n\">to</span> <span class=\"k\">with</span> <span class=\"n\">the</span> <span class=\"n\">following</span> <span class=\"n\">query</span> <span class=\"n\">parameters</span><span class=\"p\">:</span>\n<span class=\"o\">-</span> <span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"n\">the</span> <span class=\"n\">socket</span> <span class=\"nb\">id</span> <span class=\"n\">of</span> <span class=\"n\">the</span> <span class=\"n\">client</span> <span class=\"n\">that</span> <span class=\"n\">should</span> <span class=\"n\">be</span> <span class=\"n\">subscribed</span> <span class=\"n\">to</span> <span class=\"n\">the</span> <span class=\"n\">endpoint</span>\n<span class=\"o\">-</span> <span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"n\">the</span> <span class=\"n\">period</span> <span class=\"n\">length</span> <span class=\"ow\">in</span> <span class=\"n\">milliseconds</span>\n<span class=\"n\">The</span> <span class=\"n\">endpoint</span> <span class=\"n\">will</span> <span class=\"n\">then</span> <span class=\"k\">return</span> <span class=\"n\">the</span> <span class=\"nb\">hash</span> <span class=\"n\">of</span> <span class=\"n\">the</span> <span class=\"n\">subscription</span> <span class=\"nb\">object</span><span class=\"o\">.</span> <span class=\"n\">This</span> <span class=\"nb\">hash</span> <span class=\"n\">will</span> <span class=\"n\">be</span> <span class=\"n\">the</span> <span class=\"n\">event_id</span> <span class=\"n\">that</span> <span class=\"n\">the</span> <span class=\"n\">data</span> <span class=\"n\">will</span>\n<span class=\"n\">be</span> <span class=\"n\">emitted</span> <span class=\"k\">with</span><span class=\"o\">.</span> <span class=\"n\">The</span> <span class=\"n\">data</span> <span class=\"n\">will</span> <span class=\"n\">be</span> <span class=\"n\">emitted</span> <span class=\"k\">as</span> <span class=\"n\">a</span> <span class=\"n\">JSON</span> <span class=\"n\">string</span><span class=\"o\">.</span>\n</code></pre>\n</div>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">func</span><span class=\"p\">:</span> <span class=\"n\">Callable</span><span class=\"p\">[[</span><span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">system_hub</span><span class=\"o\">.</span><span class=\"n\">SystemHub</span><span class=\"p\">,</span> <span class=\"o\">...</span><span class=\"p\">],</span> <span class=\"n\">Any</span><span class=\"p\">]</span></span><span class=\"return-annotation\">) -> <span class=\"n\">Callable</span><span class=\"p\">[</span><span class=\"o\">...</span><span class=\"p\">,</span> <span class=\"n\">Any</span><span class=\"p\">]</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.api.v1",
        "modulename": "open_precision.api.v1",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.api.v1.v1_router",
        "modulename": "open_precision.api.v1",
        "qualname": "v1_router",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;fastapi.routing.APIRouter object&gt;"
    }, {
        "fullname": "open_precision.api.v1.routers",
        "modulename": "open_precision.api.v1",
        "qualname": "routers",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "[&lt;fastapi.routing.APIRouter object&gt;, &lt;fastapi.routing.APIRouter object&gt;, &lt;fastapi.routing.APIRouter object&gt;, &lt;fastapi.routing.APIRouter object&gt;, &lt;fastapi.routing.APIRouter object&gt;]"
    }, {
        "fullname": "open_precision.api.v1.config",
        "modulename": "open_precision.api.v1.config",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.api.v1.config.ConfigSchema",
        "modulename": "open_precision.api.v1.config",
        "qualname": "ConfigSchema",
        "kind": "class",
        "doc": "<p></p>\n",
        "bases": "pydantic.main.BaseModel"
    }, {
        "fullname": "open_precision.api.v1.config.ConfigSchema.content",
        "modulename": "open_precision.api.v1.config",
        "qualname": "ConfigSchema.content",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": str"
    }, {
        "fullname": "open_precision.api.v1.config.config_router",
        "modulename": "open_precision.api.v1.config",
        "qualname": "config_router",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;fastapi.routing.APIRouter object&gt;"
    }, {
        "fullname": "open_precision.api.v1.config.get_config",
        "modulename": "open_precision.api.v1.config",
        "qualname": "get_config",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span></span><span class=\"return-annotation\">) -> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">api</span><span class=\"o\">.</span><span class=\"n\">v1</span><span class=\"o\">.</span><span class=\"n\">config</span><span class=\"o\">.</span><span class=\"n\">ConfigSchema</span>:</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.config.set_config",
        "modulename": "open_precision.api.v1.config",
        "qualname": "set_config",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">config</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">api</span><span class=\"o\">.</span><span class=\"n\">v1</span><span class=\"o\">.</span><span class=\"n\">config</span><span class=\"o\">.</span><span class=\"n\">ConfigSchema</span>,</span><span class=\"param\">\t<span class=\"n\">reload</span><span class=\"p\">:</span> <span class=\"nb\">bool</span> <span class=\"o\">=</span> <span class=\"kc\">False</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.navigator",
        "modulename": "open_precision.api.v1.navigator",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.api.v1.navigator.navigator_router",
        "modulename": "open_precision.api.v1.navigator",
        "qualname": "navigator_router",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;fastapi.routing.APIRouter object&gt;"
    }, {
        "fullname": "open_precision.api.v1.navigator.get_target_steering_angle",
        "modulename": "open_precision.api.v1.navigator",
        "qualname": "get_target_steering_angle",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">float</span>:</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.navigator.generate_course",
        "modulename": "open_precision.api.v1.navigator",
        "qualname": "generate_course",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.navigator.get_current_course",
        "modulename": "open_precision.api.v1.navigator",
        "qualname": "get_current_course",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.sensor",
        "modulename": "open_precision.api.v1.sensor",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.api.v1.sensor.sensor_router",
        "modulename": "open_precision.api.v1.sensor",
        "qualname": "sensor_router",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;fastapi.routing.APIRouter object&gt;"
    }, {
        "fullname": "open_precision.api.v1.sensor.routers",
        "modulename": "open_precision.api.v1.sensor",
        "qualname": "routers",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "[&lt;fastapi.routing.APIRouter object&gt;, &lt;fastapi.routing.APIRouter object&gt;, &lt;fastapi.routing.APIRouter object&gt;]"
    }, {
        "fullname": "open_precision.api.v1.sensor.aos",
        "modulename": "open_precision.api.v1.sensor.aos",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.api.v1.sensor.aos.aos_router",
        "modulename": "open_precision.api.v1.sensor.aos",
        "qualname": "aos_router",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;fastapi.routing.APIRouter object&gt;"
    }, {
        "fullname": "open_precision.api.v1.sensor.aos.get_orientation",
        "modulename": "open_precision.api.v1.sensor.aos",
        "qualname": "get_orientation",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.sensor.aos.calibrate",
        "modulename": "open_precision.api.v1.sensor.aos",
        "qualname": "calibrate",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.sensor.gps",
        "modulename": "open_precision.api.v1.sensor.gps",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.api.v1.sensor.gps.gps_router",
        "modulename": "open_precision.api.v1.sensor.gps",
        "qualname": "gps_router",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;fastapi.routing.APIRouter object&gt;"
    }, {
        "fullname": "open_precision.api.v1.sensor.gps.get_position",
        "modulename": "open_precision.api.v1.sensor.gps",
        "qualname": "get_position",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.sensor.imu",
        "modulename": "open_precision.api.v1.sensor.imu",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.api.v1.sensor.imu.imu_router",
        "modulename": "open_precision.api.v1.sensor.imu",
        "qualname": "imu_router",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;fastapi.routing.APIRouter object&gt;"
    }, {
        "fullname": "open_precision.api.v1.sensor.imu.get_acceleration",
        "modulename": "open_precision.api.v1.sensor.imu",
        "qualname": "get_acceleration",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.sensor.imu.get_angular_acceleration",
        "modulename": "open_precision.api.v1.sensor.imu",
        "qualname": "get_angular_acceleration",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.sensor.imu.get_scaled_magnetometer",
        "modulename": "open_precision.api.v1.sensor.imu",
        "qualname": "get_scaled_magnetometer",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.system",
        "modulename": "open_precision.api.v1.system",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.api.v1.system.system_router",
        "modulename": "open_precision.api.v1.system",
        "qualname": "system_router",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;fastapi.routing.APIRouter object&gt;"
    }, {
        "fullname": "open_precision.api.v1.system.routers",
        "modulename": "open_precision.api.v1.system",
        "qualname": "routers",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "[&lt;fastapi.routing.APIRouter object&gt;, &lt;fastapi.routing.APIRouter object&gt;]"
    }, {
        "fullname": "open_precision.api.v1.system.data_subscription",
        "modulename": "open_precision.api.v1.system.data_subscription",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.api.v1.system.data_subscription.data_subscription_router",
        "modulename": "open_precision.api.v1.system.data_subscription",
        "qualname": "data_subscription_router",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;fastapi.routing.APIRouter object&gt;"
    }, {
        "fullname": "open_precision.api.v1.system.data_subscription.connect_data_subscription",
        "modulename": "open_precision.api.v1.system.data_subscription",
        "qualname": "connect_data_subscription",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">sid</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">=</span> <span class=\"n\">Body</span><span class=\"p\">(</span><span class=\"n\">PydanticUndefined</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.system.data_subscription.disconnect_data_subscription",
        "modulename": "open_precision.api.v1.system.data_subscription",
        "qualname": "disconnect_data_subscription",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">sid</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">=</span> <span class=\"n\">Body</span><span class=\"p\">(</span><span class=\"n\">PydanticUndefined</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.system.data_subscription.remove_all_data_subscriptions",
        "modulename": "open_precision.api.v1.system.data_subscription",
        "qualname": "remove_all_data_subscriptions",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">sid</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">=</span> <span class=\"n\">Body</span><span class=\"p\">(</span><span class=\"n\">PydanticUndefined</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.system.data_subscription.get_all_data_subscriptions",
        "modulename": "open_precision.api.v1.system.data_subscription",
        "qualname": "get_all_data_subscriptions",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.system.plugin",
        "modulename": "open_precision.api.v1.system.plugin",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.api.v1.system.plugin.plugin_router",
        "modulename": "open_precision.api.v1.system.plugin",
        "qualname": "plugin_router",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;fastapi.routing.APIRouter object&gt;"
    }, {
        "fullname": "open_precision.api.v1.system.plugin.get_enabled_plugins",
        "modulename": "open_precision.api.v1.system.plugin",
        "qualname": "get_enabled_plugins",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.vehicle_state",
        "modulename": "open_precision.api.v1.vehicle_state",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.api.v1.vehicle_state.vehicle_state_router",
        "modulename": "open_precision.api.v1.vehicle_state",
        "qualname": "vehicle_state_router",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;fastapi.routing.APIRouter object&gt;"
    }, {
        "fullname": "open_precision.api.v1.vehicle_state.get_vehicle_state",
        "modulename": "open_precision.api.v1.vehicle_state",
        "qualname": "get_vehicle_state",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">ignore_uuid</span><span class=\"p\">:</span> <span class=\"nb\">bool</span> <span class=\"o\">=</span> <span class=\"kc\">False</span>,</span><span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.vehicle_state.get_steering_angle",
        "modulename": "open_precision.api.v1.vehicle_state",
        "qualname": "get_steering_angle",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">float</span>:</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.vehicle_state.get_speed",
        "modulename": "open_precision.api.v1.vehicle_state",
        "qualname": "get_speed",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">float</span>:</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.api.v1.vehicle_state.get_position",
        "modulename": "open_precision.api.v1.vehicle_state",
        "qualname": "get_position",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">queue_system_task</span><span class=\"o\">=</span><span class=\"n\">Depends</span><span class=\"p\">(</span><span class=\"n\">queue_system_task_dependency</span><span class=\"p\">)</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_socket_id</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">subscription_period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.core",
        "modulename": "open_precision.core",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.exceptions",
        "modulename": "open_precision.core.exceptions",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.exceptions.MissingPluginException",
        "modulename": "open_precision.core.exceptions",
        "qualname": "MissingPluginException",
        "kind": "class",
        "doc": "<p>missing plugin</p>\n",
        "bases": "builtins.Exception"
    }, {
        "fullname": "open_precision.core.exceptions.MissingPluginException.__init__",
        "modulename": "open_precision.core.exceptions",
        "qualname": "MissingPluginException.__init__",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">missing_plugin</span><span class=\"p\">:</span> <span class=\"nb\">str</span>, </span><span class=\"param\"><span class=\"n\">plugin_package</span><span class=\"p\">:</span> <span class=\"nb\">str</span></span>)</span>"
    }, {
        "fullname": "open_precision.core.exceptions.PluginException",
        "modulename": "open_precision.core.exceptions",
        "qualname": "PluginException",
        "kind": "class",
        "doc": "<p>subclasses can be raised by plugins</p>\n",
        "bases": "builtins.Exception, abc.ABC"
    }, {
        "fullname": "open_precision.core.exceptions.SensorNotConnectedException",
        "modulename": "open_precision.core.exceptions",
        "qualname": "SensorNotConnectedException",
        "kind": "class",
        "doc": "<p>raised when trying to access a sensor that is not connected</p>\n",
        "bases": "PluginException"
    }, {
        "fullname": "open_precision.core.exceptions.SensorNotConnectedException.__init__",
        "modulename": "open_precision.core.exceptions",
        "qualname": "SensorNotConnectedException.__init__",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">sensor</span></span>)</span>"
    }, {
        "fullname": "open_precision.core.exceptions.SensorNotConnectedException.sensor",
        "modulename": "open_precision.core.exceptions",
        "qualname": "SensorNotConnectedException.sensor",
        "kind": "variable",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.exceptions.NotAPathException",
        "modulename": "open_precision.core.exceptions",
        "qualname": "NotAPathException",
        "kind": "class",
        "doc": "<p>subclasses can be raised by plugins</p>\n",
        "bases": "PluginException"
    }, {
        "fullname": "open_precision.core.exceptions.NotAPathException.__init__",
        "modulename": "open_precision.core.exceptions",
        "qualname": "NotAPathException.__init__",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">path</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">path</span><span class=\"o\">.</span><span class=\"n\">Path</span></span>)</span>"
    }, {
        "fullname": "open_precision.core.exceptions.NotAPathException.path",
        "modulename": "open_precision.core.exceptions",
        "qualname": "NotAPathException.path",
        "kind": "variable",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.exceptions.CourseNotSetException",
        "modulename": "open_precision.core.exceptions",
        "qualname": "CourseNotSetException",
        "kind": "class",
        "doc": "<p>raised when there is no course set in navigator</p>\n",
        "bases": "PluginException"
    }, {
        "fullname": "open_precision.core.exceptions.CourseNotSetException.__init__",
        "modulename": "open_precision.core.exceptions",
        "qualname": "CourseNotSetException.__init__",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">navigator</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">plugin_base_classes</span><span class=\"o\">.</span><span class=\"n\">navigator</span><span class=\"o\">.</span><span class=\"n\">Navigator</span></span>)</span>"
    }, {
        "fullname": "open_precision.core.exceptions.CourseNotSetException.navigator",
        "modulename": "open_precision.core.exceptions",
        "qualname": "CourseNotSetException.navigator",
        "kind": "variable",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.exceptions.InvalidValueException",
        "modulename": "open_precision.core.exceptions",
        "qualname": "InvalidValueException",
        "kind": "class",
        "doc": "<p>raised when a value is invalid</p>\n",
        "bases": "PluginException"
    }, {
        "fullname": "open_precision.core.exceptions.InvalidValueException.__init__",
        "modulename": "open_precision.core.exceptions",
        "qualname": "InvalidValueException.__init__",
        "kind": "function",
        "doc": "<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>value</strong>:  the invalid value</li>\n<li><strong>value_rule</strong>:  a string describing the rule that the value must follow</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">value</span><span class=\"p\">:</span> <span class=\"n\">Any</span>, </span><span class=\"param\"><span class=\"n\">value_rule</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span>)</span>"
    }, {
        "fullname": "open_precision.core.exceptions.InvalidValueException.value",
        "modulename": "open_precision.core.exceptions",
        "qualname": "InvalidValueException.value",
        "kind": "variable",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.exceptions.InvalidValueException.value_rule",
        "modulename": "open_precision.core.exceptions",
        "qualname": "InvalidValueException.value_rule",
        "kind": "variable",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.model",
        "modulename": "open_precision.core.model",
        "kind": "module",
        "doc": "<p>model graph infrastructure:\n<a href=\"https://arrows.app/#/import/json=eyJncmFwaCI6eyJzdHlsZSI6eyJmb250LWZhbWlseSI6InNhbnMtc2VyaWYiLCJiYWNrZ3JvdW5kLWNvbG9yIjoiI2ZmZmZmZiIsImJhY2tncm91bmQtaW1hZ2UiOiIiLCJiYWNrZ3JvdW5kLXNpemUiOiIxMDAlIiwibm9kZS1jb2xvciI6IiNmZmZmZmYiLCJib3JkZXItd2lkdGgiOjQsImJvcmRlci1jb2xvciI6IiMwMDAwMDAiLCJyYWRpdXMiOjUwLCJub2RlLXBhZGRpbmciOjUsIm5vZGUtbWFyZ2luIjoyLCJvdXRzaWRlLXBvc2l0aW9uIjoiYXV0byIsIm5vZGUtaWNvbi1pbWFnZSI6IiIsIm5vZGUtYmFja2dyb3VuZC1pbWFnZSI6IiIsImljb24tcG9zaXRpb24iOiJpbnNpZGUiLCJpY29uLXNpemUiOjY0LCJjYXB0aW9uLXBvc2l0aW9uIjoiaW5zaWRlIiwiY2FwdGlvbi1tYXgtd2lkdGgiOjIwMCwiY2FwdGlvbi1jb2xvciI6IiMwMDAwMDAiLCJjYXB0aW9uLWZvbnQtc2l6ZSI6NTAsImNhcHRpb24tZm9udC13ZWlnaHQiOiJub3JtYWwiLCJsYWJlbC1wb3NpdGlvbiI6Imluc2lkZSIsImxhYmVsLWRpc3BsYXkiOiJwaWxsIiwibGFiZWwtY29sb3IiOiIjMDAwMDAwIiwibGFiZWwtYmFja2dyb3VuZC1jb2xvciI6IiNmZmZmZmYiLCJsYWJlbC1ib3JkZXItY29sb3IiOiIjMDAwMDAwIiwibGFiZWwtYm9yZGVyLXdpZHRoIjo0LCJsYWJlbC1mb250LXNpemUiOjQwLCJsYWJlbC1wYWRkaW5nIjo1LCJsYWJlbC1tYXJnaW4iOjQsImRpcmVjdGlvbmFsaXR5IjoiZGlyZWN0ZWQiLCJkZXRhaWwtcG9zaXRpb24iOiJpbmxpbmUiLCJkZXRhaWwtb3JpZW50YXRpb24iOiJwYXJhbGxlbCIsImFycm93LXdpZHRoIjo1LCJhcnJvdy1jb2xvciI6IiMwMDAwMDAiLCJtYXJnaW4tc3RhcnQiOjUsIm1hcmdpbi1lbmQiOjUsIm1hcmdpbi1wZWVyIjoyMCwiYXR0YWNobWVudC1zdGFydCI6Im5vcm1hbCIsImF0dGFjaG1lbnQtZW5kIjoibm9ybWFsIiwicmVsYXRpb25zaGlwLWljb24taW1hZ2UiOiIiLCJ0eXBlLWNvbG9yIjoiIzAwMDAwMCIsInR5cGUtYmFja2dyb3VuZC1jb2xvciI6IiNmZmZmZmYiLCJ0eXBlLWJvcmRlci1jb2xvciI6IiMwMDAwMDAiLCJ0eXBlLWJvcmRlci13aWR0aCI6MCwidHlwZS1mb250LXNpemUiOjE2LCJ0eXBlLXBhZGRpbmciOjUsInByb3BlcnR5LXBvc2l0aW9uIjoib3V0c2lkZSIsInByb3BlcnR5LWFsaWdubWVudCI6ImNvbG9uIiwicHJvcGVydHktY29sb3IiOiIjMDAwMDAwIiwicHJvcGVydHktZm9udC1zaXplIjoxNiwicHJvcGVydHktZm9udC13ZWlnaHQiOiJub3JtYWwifSwibm9kZXMiOlt7ImlkIjoibjAiLCJwb3NpdGlvbiI6eyJ4IjotNC4xMjQzMzk0MDIzMjAxMDllLTMyLCJ5IjotMzAuNTYwOTQ5MjEyNTE5MDM0fSwiY2FwdGlvbiI6IiIsImxhYmVscyI6WyJBY3Rpb24iXSwicHJvcGVydGllcyI6eyJpZCI6InN0ciIsImluaXRpYXRvciI6InN0ciIsImZ1bmN0aW9uX2lkZW50aWZpZXIiOiJzdHIiLCJhcmdzIjoiTGlzdFtBbnldIiwia3dfYXJncyI6IkRpY3Rbc3RyLCBBbnldIn0sInN0eWxlIjp7fX0seyJpZCI6Im4xIiwicG9zaXRpb24iOnsieCI6MCwieSI6MzAwfSwiY2FwdGlvbiI6IiIsImxhYmVscyI6WyJBY3Rpb25fcmVzcG9uc2UiXSwicHJvcGVydGllcyI6eyJpZCI6InN0ciIsInN1Y2Nlc3MiOiJib29sIiwicmVzcG9uc2UiOiJzdHIifSwic3R5bGUiOnt9fSx7ImlkIjoibjIiLCJwb3NpdGlvbiI6eyJ4IjozMDAsInkiOi0zMC41NjA5NDkyMTI1MTkwMzR9LCJjYXB0aW9uIjoiIiwibGFiZWxzIjpbIkNvdXJzZSJdLCJwcm9wZXJ0aWVzIjp7ImlkIjoic3RyIiwibmFtZSI6InN0ciIsImRlc2NyaXB0aW9uIjoic3RyIn0sInN0eWxlIjp7fX0seyJpZCI6Im40IiwicG9zaXRpb24iOnsieCI6NjAwLCJ5IjoyMTguNDAxNTU5NzQxNjEzfSwiY2FwdGlvbiI6IiIsImxhYmVscyI6WyJXYXlwb2ludCJdLCJwcm9wZXJ0aWVzIjp7ImlkIjoic3RyIiwibG9jYXRpb24iOiJMb2NhdGlvbiJ9LCJzdHlsZSI6e319LHsiaWQiOiJuNSIsInBvc2l0aW9uIjp7IngiOjQyMSwieSI6NDExfSwiY2FwdGlvbiI6IiIsImxhYmVscyI6WyJWZWhpY2xlIl0sInByb3BlcnRpZXMiOnsiaWQiOiJzdHIiLCJuYW1lIjoic3RyIiwidHVybl9yYWRpdXNfbGVmdCI6ImZsb2F0IiwidHVybl9yYWRpdXNfcmlnaHQiOiJmbG9hdCIsIndoZWVsYmFzZSI6ImZsb2F0IiwiZ3BzX3JlY2VpdmVyX29mZnNldCI6Ikxpc3RbZmxvYXRdIn0sInN0eWxlIjp7fX0seyJpZCI6Im43IiwicG9zaXRpb24iOnsieCI6NjMxLjY1MDE2MjM0NTczMzEsInkiOi0zMC41NjA5NDkyMTI1MTkwMzR9LCJjYXB0aW9uIjoiIiwic3R5bGUiOnt9LCJsYWJlbHMiOlsiUGF0aCJdLCJwcm9wZXJ0aWVzIjp7ImlkIjoic3RyIn19LHsiaWQiOiJuOCIsInBvc2l0aW9uIjp7IngiOjc0NywieSI6NjEyfSwiY2FwdGlvbiI6IiIsInN0eWxlIjp7fSwibGFiZWxzIjpbIlZlaGljbGVTdGF0ZSJdLCJwcm9wZXJ0aWVzIjp7ImlkIjoic3RyIiwic3RlZXJpbmdfYW5nbGUiOiJmbG9hdCIsInNwZWVkIjoiZmxvYXQiLCJwb3NpdGlvbiI6IlBvc2l0aW9uIn19XSwicmVsYXRpb25zaGlwcyI6W3siaWQiOiJuMCIsImZyb21JZCI6Im4wIiwidG9JZCI6Im4xIiwidHlwZSI6InJldHVybnMiLCJwcm9wZXJ0aWVzIjp7fSwic3R5bGUiOnt9fSx7ImlkIjoibjIiLCJ0eXBlIjoiU1VDQ0VTU09SIiwic3R5bGUiOnt9LCJwcm9wZXJ0aWVzIjp7fSwiZnJvbUlkIjoibjQiLCJ0b0lkIjoibjQifSx7ImlkIjoibjYiLCJ0eXBlIjoiQ09OVEFJTlMiLCJzdHlsZSI6e30sInByb3BlcnRpZXMiOnt9LCJmcm9tSWQiOiJuMiIsInRvSWQiOiJuNCJ9LHsiaWQiOiJuNyIsInR5cGUiOiJDT05UQUlOUyIsInN0eWxlIjp7fSwicHJvcGVydGllcyI6e30sImZyb21JZCI6Im4yIiwidG9JZCI6Im43In0seyJpZCI6Im44IiwidHlwZSI6IkNPTlRBSU5TIiwic3R5bGUiOnt9LCJwcm9wZXJ0aWVzIjp7fSwiZnJvbUlkIjoibjciLCJ0b0lkIjoibjQifSx7ImlkIjoibjkiLCJ0eXBlIjoiUkVRVUlSRVMiLCJzdHlsZSI6e30sInByb3BlcnRpZXMiOnt9LCJmcm9tSWQiOiJuNyIsInRvSWQiOiJuNyJ9XX0sImRpYWdyYW1OYW1lIjoiSW1wb3J0ZWQgZnJvbSBodHRwczovL3d3dy5hcGNqb25lcy5jb20vYXJyb3dzLyJ9\">https://arrows.app/#/import/json=eyJncmFwaCI6eyJzdHlsZSI6eyJmb250LWZhbWlseSI6InNhbnMtc2VyaWYiLCJiYWNrZ3JvdW5kLWNvbG9yIjoiI2ZmZmZmZiIsImJhY2tncm91bmQtaW1hZ2UiOiIiLCJiYWNrZ3JvdW5kLXNpemUiOiIxMDAlIiwibm9kZS1jb2xvciI6IiNmZmZmZmYiLCJib3JkZXItd2lkdGgiOjQsImJvcmRlci1jb2xvciI6IiMwMDAwMDAiLCJyYWRpdXMiOjUwLCJub2RlLXBhZGRpbmciOjUsIm5vZGUtbWFyZ2luIjoyLCJvdXRzaWRlLXBvc2l0aW9uIjoiYXV0byIsIm5vZGUtaWNvbi1pbWFnZSI6IiIsIm5vZGUtYmFja2dyb3VuZC1pbWFnZSI6IiIsImljb24tcG9zaXRpb24iOiJpbnNpZGUiLCJpY29uLXNpemUiOjY0LCJjYXB0aW9uLXBvc2l0aW9uIjoiaW5zaWRlIiwiY2FwdGlvbi1tYXgtd2lkdGgiOjIwMCwiY2FwdGlvbi1jb2xvciI6IiMwMDAwMDAiLCJjYXB0aW9uLWZvbnQtc2l6ZSI6NTAsImNhcHRpb24tZm9udC13ZWlnaHQiOiJub3JtYWwiLCJsYWJlbC1wb3NpdGlvbiI6Imluc2lkZSIsImxhYmVsLWRpc3BsYXkiOiJwaWxsIiwibGFiZWwtY29sb3IiOiIjMDAwMDAwIiwibGFiZWwtYmFja2dyb3VuZC1jb2xvciI6IiNmZmZmZmYiLCJsYWJlbC1ib3JkZXItY29sb3IiOiIjMDAwMDAwIiwibGFiZWwtYm9yZGVyLXdpZHRoIjo0LCJsYWJlbC1mb250LXNpemUiOjQwLCJsYWJlbC1wYWRkaW5nIjo1LCJsYWJlbC1tYXJnaW4iOjQsImRpcmVjdGlvbmFsaXR5IjoiZGlyZWN0ZWQiLCJkZXRhaWwtcG9zaXRpb24iOiJpbmxpbmUiLCJkZXRhaWwtb3JpZW50YXRpb24iOiJwYXJhbGxlbCIsImFycm93LXdpZHRoIjo1LCJhcnJvdy1jb2xvciI6IiMwMDAwMDAiLCJtYXJnaW4tc3RhcnQiOjUsIm1hcmdpbi1lbmQiOjUsIm1hcmdpbi1wZWVyIjoyMCwiYXR0YWNobWVudC1zdGFydCI6Im5vcm1hbCIsImF0dGFjaG1lbnQtZW5kIjoibm9ybWFsIiwicmVsYXRpb25zaGlwLWljb24taW1hZ2UiOiIiLCJ0eXBlLWNvbG9yIjoiIzAwMDAwMCIsInR5cGUtYmFja2dyb3VuZC1jb2xvciI6IiNmZmZmZmYiLCJ0eXBlLWJvcmRlci1jb2xvciI6IiMwMDAwMDAiLCJ0eXBlLWJvcmRlci13aWR0aCI6MCwidHlwZS1mb250LXNpemUiOjE2LCJ0eXBlLXBhZGRpbmciOjUsInByb3BlcnR5LXBvc2l0aW9uIjoib3V0c2lkZSIsInByb3BlcnR5LWFsaWdubWVudCI6ImNvbG9uIiwicHJvcGVydHktY29sb3IiOiIjMDAwMDAwIiwicHJvcGVydHktZm9udC1zaXplIjoxNiwicHJvcGVydHktZm9udC13ZWlnaHQiOiJub3JtYWwifSwibm9kZXMiOlt7ImlkIjoibjAiLCJwb3NpdGlvbiI6eyJ4IjotNC4xMjQzMzk0MDIzMjAxMDllLTMyLCJ5IjotMzAuNTYwOTQ5MjEyNTE5MDM0fSwiY2FwdGlvbiI6IiIsImxhYmVscyI6WyJBY3Rpb24iXSwicHJvcGVydGllcyI6eyJpZCI6InN0ciIsImluaXRpYXRvciI6InN0ciIsImZ1bmN0aW9uX2lkZW50aWZpZXIiOiJzdHIiLCJhcmdzIjoiTGlzdFtBbnldIiwia3dfYXJncyI6IkRpY3Rbc3RyLCBBbnldIn0sInN0eWxlIjp7fX0seyJpZCI6Im4xIiwicG9zaXRpb24iOnsieCI6MCwieSI6MzAwfSwiY2FwdGlvbiI6IiIsImxhYmVscyI6WyJBY3Rpb25fcmVzcG9uc2UiXSwicHJvcGVydGllcyI6eyJpZCI6InN0ciIsInN1Y2Nlc3MiOiJib29sIiwicmVzcG9uc2UiOiJzdHIifSwic3R5bGUiOnt9fSx7ImlkIjoibjIiLCJwb3NpdGlvbiI6eyJ4IjozMDAsInkiOi0zMC41NjA5NDkyMTI1MTkwMzR9LCJjYXB0aW9uIjoiIiwibGFiZWxzIjpbIkNvdXJzZSJdLCJwcm9wZXJ0aWVzIjp7ImlkIjoic3RyIiwibmFtZSI6InN0ciIsImRlc2NyaXB0aW9uIjoic3RyIn0sInN0eWxlIjp7fX0seyJpZCI6Im40IiwicG9zaXRpb24iOnsieCI6NjAwLCJ5IjoyMTguNDAxNTU5NzQxNjEzfSwiY2FwdGlvbiI6IiIsImxhYmVscyI6WyJXYXlwb2ludCJdLCJwcm9wZXJ0aWVzIjp7ImlkIjoic3RyIiwibG9jYXRpb24iOiJMb2NhdGlvbiJ9LCJzdHlsZSI6e319LHsiaWQiOiJuNSIsInBvc2l0aW9uIjp7IngiOjQyMSwieSI6NDExfSwiY2FwdGlvbiI6IiIsImxhYmVscyI6WyJWZWhpY2xlIl0sInByb3BlcnRpZXMiOnsiaWQiOiJzdHIiLCJuYW1lIjoic3RyIiwidHVybl9yYWRpdXNfbGVmdCI6ImZsb2F0IiwidHVybl9yYWRpdXNfcmlnaHQiOiJmbG9hdCIsIndoZWVsYmFzZSI6ImZsb2F0IiwiZ3BzX3JlY2VpdmVyX29mZnNldCI6Ikxpc3RbZmxvYXRdIn0sInN0eWxlIjp7fX0seyJpZCI6Im43IiwicG9zaXRpb24iOnsieCI6NjMxLjY1MDE2MjM0NTczMzEsInkiOi0zMC41NjA5NDkyMTI1MTkwMzR9LCJjYXB0aW9uIjoiIiwic3R5bGUiOnt9LCJsYWJlbHMiOlsiUGF0aCJdLCJwcm9wZXJ0aWVzIjp7ImlkIjoic3RyIn19LHsiaWQiOiJuOCIsInBvc2l0aW9uIjp7IngiOjc0NywieSI6NjEyfSwiY2FwdGlvbiI6IiIsInN0eWxlIjp7fSwibGFiZWxzIjpbIlZlaGljbGVTdGF0ZSJdLCJwcm9wZXJ0aWVzIjp7ImlkIjoic3RyIiwic3RlZXJpbmdfYW5nbGUiOiJmbG9hdCIsInNwZWVkIjoiZmxvYXQiLCJwb3NpdGlvbiI6IlBvc2l0aW9uIn19XSwicmVsYXRpb25zaGlwcyI6W3siaWQiOiJuMCIsImZyb21JZCI6Im4wIiwidG9JZCI6Im4xIiwidHlwZSI6InJldHVybnMiLCJwcm9wZXJ0aWVzIjp7fSwic3R5bGUiOnt9fSx7ImlkIjoibjIiLCJ0eXBlIjoiU1VDQ0VTU09SIiwic3R5bGUiOnt9LCJwcm9wZXJ0aWVzIjp7fSwiZnJvbUlkIjoibjQiLCJ0b0lkIjoibjQifSx7ImlkIjoibjYiLCJ0eXBlIjoiQ09OVEFJTlMiLCJzdHlsZSI6e30sInByb3BlcnRpZXMiOnt9LCJmcm9tSWQiOiJuMiIsInRvSWQiOiJuNCJ9LHsiaWQiOiJuNyIsInR5cGUiOiJDT05UQUlOUyIsInN0eWxlIjp7fSwicHJvcGVydGllcyI6e30sImZyb21JZCI6Im4yIiwidG9JZCI6Im43In0seyJpZCI6Im44IiwidHlwZSI6IkNPTlRBSU5TIiwic3R5bGUiOnt9LCJwcm9wZXJ0aWVzIjp7fSwiZnJvbUlkIjoibjciLCJ0b0lkIjoibjQifSx7ImlkIjoibjkiLCJ0eXBlIjoiUkVRVUlSRVMiLCJzdHlsZSI6e30sInByb3BlcnRpZXMiOnt9LCJmcm9tSWQiOiJuNyIsInRvSWQiOiJuNyJ9XX0sImRpYWdyYW1OYW1lIjoiSW1wb3J0ZWQgZnJvbSBodHRwczovL3d3dy5hcGNqb25lcy5jb20vYXJyb3dzLyJ9</a></p>\n\n<h1 id=\"the-model-implementation\">The Model Implementation</h1>\n\n<p>The model consists of nodes and data classes (they <strong>don't</strong> need to be a dataclasses.dataclass)).\nBoth types of classes need to inherit from DataModelBase, which supplies serialization and deserialization methods.\nAll model classes must be in the data_model_classes list below.</p>\n\n<h2 id=\"nodes\">Nodes</h2>\n\n<p>Nodes are classes that inherit from StructuredNode. They are stored and queried in the graph database (neo4j).\nTo store them in the data base, use the .save() method of the object you want to store. To learn more about persistence,\nlook up the neomodel documentation.\nThe object graph mapper is neomodel, classes that should represent classes must inherit from neomodel.StructuredNode.\nThe annotation of class attribute show the datatype, the property type assigned to the attribute describes how the data\ntype is stored.</p>\n\n<h3 id=\"adding-nodes\">Adding Nodes</h3>\n\n<p>To add a node, create a module with a class that inherits from neomodel.StructuredNode and DataModelBase, then add the class to the data_model_classes list in this module (the module import must happen in the map_model func).\nThe class attributes are the properties of the node.\nThe annotation of the class attribute shows the datatype of the property.\nThe value assigned to that attribute describes how the data type is stored and must be of neomodel.Property.\nIf the attribute should for example be data class as described below, the data class will be used in the type annotation, while the corresponding Property class will be used as the value assigned to the attribute.</p>\n\n<h2 id=\"data-classes\">Data Classes</h2>\n\n<p>Data classes that won't be explicitly stored as single nodes in the graph but can be stored as properties of nodes.\nEvery data class also needs a corresponding property class that maps the data class attributes to a neo4j supported data type.\nThese Property classes should be defined in the same module as the corresponding data class and must inherit from neomodel.Property (and implement the inflate and deflate methods).\nThe inflate method takes the value stored in the database and returns the data class, the deflate method takes the data class and returns the value that should be stored in the database.</p>\n\n<h3 id=\"adding-data-classes\">Adding Data Classes</h3>\n\n<p>To add a data class, create a module with a class that inherits from DataModelBase and is decorated with dataclasses.dataclass(kw_only=True).\nAll attributes must have a value assigned to them in the class definition.\nIn that same module create a class that inherits from neomodel.Property and implement the inflate and deflate methods to inflate/deflate an object from/into a neo4j native type.</p>\n\n<h1 id=\"json-serialization\">JSON Serialization</h1>\n\n<p>Use the to_json method of DataModelBase objects or the CustomJSONEncoder class to serialize the object to json.\nUse the from_json method of DataModelBase class or the CustomJSONDecoder class to deserialize the json string to an object.\nThe CustomJSONDecoder uses duck typing to determine the class of the object (more specifically, it uses the names of the class attributes (except relationships)).</p>\n\n<p>Both serialization and deserialization ignore all relationships.</p>\n"
    }, {
        "fullname": "open_precision.core.model.signature_class_mapping",
        "modulename": "open_precision.core.model",
        "qualname": "signature_class_mapping",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": dict"
    }, {
        "fullname": "open_precision.core.model.class_signature_mapping",
        "modulename": "open_precision.core.model",
        "qualname": "class_signature_mapping",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": dict"
    }, {
        "fullname": "open_precision.core.model.persist_return",
        "modulename": "open_precision.core.model",
        "qualname": "persist_return",
        "kind": "function",
        "doc": "<p>this decorator will persist the return value of the decorated func when it is called</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">func</span><span class=\"p\">:</span> <span class=\"o\">&lt;</span><span class=\"n\">built</span><span class=\"o\">-</span><span class=\"ow\">in</span> <span class=\"n\">function</span> <span class=\"nb\">callable</span><span class=\"o\">&gt;</span></span><span class=\"return-annotation\">) -> <span class=\"o\">&lt;</span><span class=\"n\">built</span><span class=\"o\">-</span><span class=\"ow\">in</span> <span class=\"n\">function</span> <span class=\"nb\">callable</span><span class=\"o\">&gt;</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.persist_arg",
        "modulename": "open_precision.core.model",
        "qualname": "persist_arg",
        "kind": "function",
        "doc": "<p>this decorator will persist the argument of the decorated func when it is called</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>func</strong>:  the func to decorate</li>\n<li><strong>position_or_kw</strong>:  the position or keyword of the argument to persist, defaults to 0</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">func</span><span class=\"p\">:</span> <span class=\"o\">&lt;</span><span class=\"n\">built</span><span class=\"o\">-</span><span class=\"ow\">in</span> <span class=\"n\">function</span> <span class=\"nb\">callable</span><span class=\"o\">&gt;</span>,</span><span class=\"param\">\t<span class=\"n\">position_or_kw</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">|</span> <span class=\"nb\">str</span> <span class=\"o\">=</span> <span class=\"mi\">0</span></span><span class=\"return-annotation\">) -> <span class=\"o\">&lt;</span><span class=\"n\">built</span><span class=\"o\">-</span><span class=\"ow\">in</span> <span class=\"n\">function</span> <span class=\"nb\">callable</span><span class=\"o\">&gt;</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.DataModelBase",
        "modulename": "open_precision.core.model",
        "qualname": "DataModelBase",
        "kind": "class",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.model.DataModelBase.to_json",
        "modulename": "open_precision.core.model",
        "qualname": "DataModelBase.to_json",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span>,</span><span class=\"param\">\t<span class=\"n\">with_rels</span><span class=\"p\">:</span> <span class=\"n\">List</span><span class=\"p\">[</span><span class=\"n\">neomodel</span><span class=\"o\">.</span><span class=\"n\">relationship_manager</span><span class=\"o\">.</span><span class=\"n\">RelationshipDefinition</span><span class=\"p\">]</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">field_key_filter</span><span class=\"p\">:</span> <span class=\"n\">Callable</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">field_type_filter</span><span class=\"p\">:</span> <span class=\"n\">Callable</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">str</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.DataModelBase.from_json",
        "modulename": "open_precision.core.model",
        "qualname": "DataModelBase.from_json",
        "kind": "function",
        "doc": "<p>Deserializes a json string to an object of the class. If the json string is a composite object (i.e. it contains\nconnections), the main object is returned.\nIf an object with the same uuid already exists in the database, it will be updated to have the properties of the\nserialized object and returned instead of a new object.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>json_string</strong>: </li>\n<li><strong>with_conns</strong>: </li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">cls</span>, </span><span class=\"param\"><span class=\"n\">json_string</span><span class=\"p\">:</span> <span class=\"nb\">str</span>, </span><span class=\"param\"><span class=\"n\">with_conns</span><span class=\"p\">:</span> <span class=\"nb\">bool</span> <span class=\"o\">=</span> <span class=\"kc\">False</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.CustomJSONEncoder",
        "modulename": "open_precision.core.model",
        "qualname": "CustomJSONEncoder",
        "kind": "class",
        "doc": "<p>Extensible JSON <a href=\"https://json.org\">https://json.org</a> encoder for Python data structures.</p>\n\n<p>Supports the following objects and types by default:</p>\n\n<p>+-------------------+---------------+\n| Python            | JSON          |\n+===================+===============+\n| dict              | object        |\n+-------------------+---------------+\n| list, tuple       | array         |\n+-------------------+---------------+\n| str               | string        |\n+-------------------+---------------+\n| int, float        | number        |\n+-------------------+---------------+\n| True              | true          |\n+-------------------+---------------+\n| False             | false         |\n+-------------------+---------------+\n| None              | null          |\n+-------------------+---------------+</p>\n\n<p>To extend this to recognize other objects, subclass and implement a\n<code>.default()</code> method with another method that returns a serializable\nobject for <code>o</code> if possible, otherwise it should call the superclass\nimplementation (to raise <code>TypeError</code>).</p>\n",
        "bases": "json.encoder.JSONEncoder"
    }, {
        "fullname": "open_precision.core.model.CustomJSONEncoder.__init__",
        "modulename": "open_precision.core.model",
        "qualname": "CustomJSONEncoder.__init__",
        "kind": "function",
        "doc": "<p>Constructor for JSONEncoder, with sensible defaults.</p>\n\n<p>If skipkeys is false, then it is a TypeError to attempt\nencoding of keys that are not str, int, float or None.  If\nskipkeys is True, such items are simply skipped.</p>\n\n<p>If ensure_ascii is true, the output is guaranteed to be str\nobjects with all incoming non-ASCII characters escaped.  If\nensure_ascii is false, the output can contain non-ASCII characters.</p>\n\n<p>If check_circular is true, then lists, dicts, and custom encoded\nobjects will be checked for circular references during encoding to\nprevent an infinite recursion (which would cause an RecursionError).\nOtherwise, no such check takes place.</p>\n\n<p>If allow_nan is true, then NaN, Infinity, and -Infinity will be\nencoded as such.  This behavior is not JSON specification compliant,\nbut is consistent with most JavaScript based encoders and decoders.\nOtherwise, it will be a ValueError to encode such floats.</p>\n\n<p>If sort_keys is true, then the output of dictionaries will be\nsorted by key; this is useful for regression tests to ensure\nthat JSON serializations can be compared on a day-to-day basis.</p>\n\n<p>If indent is a non-negative integer, then JSON array\nelements and object members will be pretty-printed with that\nindent level.  An indent level of 0 will only insert newlines.\nNone is the most compact representation.</p>\n\n<p>If specified, separators should be an (item_separator, key_separator)\ntuple.  The default is (', ', ': ') if <em>indent</em> is <code>None</code> and\n(',', ': ') otherwise.  To get the most compact JSON representation,\nyou should specify (',', ':') to eliminate whitespace.</p>\n\n<p>If specified, default is a function that gets called for objects\nthat can't otherwise be serialized.  It should return a JSON encodable\nversion of the object or raise a <code>TypeError</code>.</p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span><span class=\"n\">args</span>,</span><span class=\"param\">\t<span class=\"n\">field_key_filter</span><span class=\"p\">:</span> <span class=\"n\">Callable</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">field_type_filter</span><span class=\"p\">:</span> <span class=\"n\">Callable</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"o\">**</span><span class=\"n\">kwargs</span></span>)</span>"
    }, {
        "fullname": "open_precision.core.model.CustomJSONEncoder.field_key_filter",
        "modulename": "open_precision.core.model",
        "qualname": "CustomJSONEncoder.field_key_filter",
        "kind": "variable",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.model.CustomJSONEncoder.field_type_filter",
        "modulename": "open_precision.core.model",
        "qualname": "CustomJSONEncoder.field_type_filter",
        "kind": "variable",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.model.CustomJSONEncoder.default",
        "modulename": "open_precision.core.model",
        "qualname": "CustomJSONEncoder.default",
        "kind": "function",
        "doc": "<p>Implement this method in a subclass such that it returns\na serializable object for <code>o</code>, or calls the base implementation\n(to raise a <code>TypeError</code>).</p>\n\n<p>For example, to support arbitrary iterators, you could\nimplement default like this::</p>\n\n<pre><code>def default(self, o):\n    try:\n        iterable = iter(o)\n    except TypeError:\n        pass\n    else:\n        return list(iterable)\n    # Let the base class default method raise the TypeError\n    return JSONEncoder.default(self, o)\n</code></pre>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">obj</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.CustomJSONDecoder",
        "modulename": "open_precision.core.model",
        "qualname": "CustomJSONDecoder",
        "kind": "class",
        "doc": "<p>JSON decoder that is able to reconstruct subclasses of DataModelBase from JSON by matching keys with class attribute\nnames. Relationship fields will be ignored.</p>\n",
        "bases": "json.decoder.JSONDecoder"
    }, {
        "fullname": "open_precision.core.model.CustomJSONDecoder.__init__",
        "modulename": "open_precision.core.model",
        "qualname": "CustomJSONDecoder.__init__",
        "kind": "function",
        "doc": "<p><code>object_hook</code>, if specified, will be called with the result\nof every JSON object decoded and its return value will be used in\nplace of the given <code>dict</code>.  This can be used to provide custom\ndeserializations (e.g. to support JSON-RPC class hinting).</p>\n\n<p><code>object_pairs_hook</code>, if specified will be called with the result of\nevery JSON object decoded with an ordered list of pairs.  The return\nvalue of <code>object_pairs_hook</code> will be used instead of the <code>dict</code>.\nThis feature can be used to implement custom decoders.\nIf <code>object_hook</code> is also defined, the <code>object_pairs_hook</code> takes\npriority.</p>\n\n<p><code>parse_float</code>, if specified, will be called with the string\nof every JSON float to be decoded. By default this is equivalent to\nfloat(num_str). This can be used to use another datatype or parser\nfor JSON floats (e.g. decimal.Decimal).</p>\n\n<p><code>parse_int</code>, if specified, will be called with the string\nof every JSON int to be decoded. By default this is equivalent to\nint(num_str). This can be used to use another datatype or parser\nfor JSON integers (e.g. float).</p>\n\n<p><code>parse_constant</code>, if specified, will be called with one of the\nfollowing strings: -Infinity, Infinity, NaN.\nThis can be used to raise an exception if invalid JSON numbers\nare encountered.</p>\n\n<p>If <code>strict</code> is false (true is the default), then control\ncharacters will be allowed inside strings.  Control characters in\nthis context are those with character codes in the 0-31 range,\nincluding <code>'\\t'</code> (tab), <code>'\\n'</code>, <code>'\\r'</code> and <code>'\\0'</code>.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"o\">*</span><span class=\"n\">args</span>, </span><span class=\"param\"><span class=\"o\">**</span><span class=\"n\">kwargs</span></span>)</span>"
    }, {
        "fullname": "open_precision.core.model.CustomJSONDecoder.object_hook",
        "modulename": "open_precision.core.model",
        "qualname": "CustomJSONDecoder.object_hook",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">obj</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.CustomJSONProperty",
        "modulename": "open_precision.core.model",
        "qualname": "CustomJSONProperty",
        "kind": "class",
        "doc": "<p>Property for storing specific data types as JSON objects in Neo4j</p>\n",
        "bases": "neomodel.properties.JSONProperty"
    }, {
        "fullname": "open_precision.core.model.CustomJSONProperty.__init__",
        "modulename": "open_precision.core.model",
        "qualname": "CustomJSONProperty.__init__",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"o\">*</span><span class=\"n\">args</span>, </span><span class=\"param\"><span class=\"o\">**</span><span class=\"n\">kwargs</span></span>)</span>"
    }, {
        "fullname": "open_precision.core.model.CustomJSONProperty.inflate",
        "modulename": "open_precision.core.model",
        "qualname": "CustomJSONProperty.inflate",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">value</span><span class=\"p\">:</span> <span class=\"nb\">str</span></span><span class=\"return-annotation\">) -> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">DataModelBase</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.CustomJSONProperty.deflate",
        "modulename": "open_precision.core.model",
        "qualname": "CustomJSONProperty.deflate",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">value</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">DataModelBase</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">str</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.map_model",
        "modulename": "open_precision.core.model",
        "qualname": "map_model",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">database_url</span><span class=\"p\">:</span> <span class=\"nb\">str</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.action",
        "modulename": "open_precision.core.model.action",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.model.action.Action",
        "modulename": "open_precision.core.model.action",
        "qualname": "Action",
        "kind": "class",
        "doc": "<p>Base class for all node definitions to inherit from.</p>\n\n<p>If you want to create your own abstract classes set:\n    __abstract_node__ = True</p>\n",
        "bases": "neomodel.core.StructuredNode, open_precision.core.model.DataModelBase"
    }, {
        "fullname": "open_precision.core.model.action.Action.uuid",
        "modulename": "open_precision.core.model.action",
        "qualname": "Action.uuid",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": str",
        "default_value": "&lt;neomodel.properties.UniqueIdProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.action.Action.initiator",
        "modulename": "open_precision.core.model.action",
        "qualname": "Action.initiator",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": str",
        "default_value": "&lt;neomodel.properties.StringProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.action.Action.function_identifier",
        "modulename": "open_precision.core.model.action",
        "qualname": "Action.function_identifier",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": str",
        "default_value": "&lt;neomodel.properties.StringProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.action.Action.args",
        "modulename": "open_precision.core.model.action",
        "qualname": "Action.args",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": List[Any]",
        "default_value": "&lt;neomodel.properties.JSONProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.action.Action.kw_args",
        "modulename": "open_precision.core.model.action",
        "qualname": "Action.kw_args",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": Dict[str, Any]",
        "default_value": "&lt;neomodel.properties.JSONProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.action.Action.RESPONDS_TO",
        "modulename": "open_precision.core.model.action",
        "qualname": "Action.RESPONDS_TO",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": neomodel.relationship_manager.RelationshipFrom",
        "default_value": "&lt;neomodel.relationship_manager.RelationshipFrom object&gt;"
    }, {
        "fullname": "open_precision.core.model.action.Action.DoesNotExist",
        "modulename": "open_precision.core.model.action",
        "qualname": "Action.DoesNotExist",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;class &#x27;neomodel.core.ActionDoesNotExist&#x27;&gt;"
    }, {
        "fullname": "open_precision.core.model.action_response",
        "modulename": "open_precision.core.model.action_response",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.model.action_response.ActionResponse",
        "modulename": "open_precision.core.model.action_response",
        "qualname": "ActionResponse",
        "kind": "class",
        "doc": "<p>Base class for all node definitions to inherit from.</p>\n\n<p>If you want to create your own abstract classes set:\n    __abstract_node__ = True</p>\n",
        "bases": "neomodel.core.StructuredNode, open_precision.core.model.DataModelBase"
    }, {
        "fullname": "open_precision.core.model.action_response.ActionResponse.uuid",
        "modulename": "open_precision.core.model.action_response",
        "qualname": "ActionResponse.uuid",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": str",
        "default_value": "&lt;neomodel.properties.UniqueIdProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.action_response.ActionResponse.success",
        "modulename": "open_precision.core.model.action_response",
        "qualname": "ActionResponse.success",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": bool",
        "default_value": "&lt;neomodel.properties.BooleanProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.action_response.ActionResponse.response",
        "modulename": "open_precision.core.model.action_response",
        "qualname": "ActionResponse.response",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": &lt;built-in function any&gt;",
        "default_value": "&lt;neomodel.properties.JSONProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.action_response.ActionResponse.RESPONDS_TO",
        "modulename": "open_precision.core.model.action_response",
        "qualname": "ActionResponse.RESPONDS_TO",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": open_precision.core.model.action.Action",
        "default_value": "&lt;neomodel.relationship_manager.RelationshipTo object&gt;"
    }, {
        "fullname": "open_precision.core.model.action_response.ActionResponse.DoesNotExist",
        "modulename": "open_precision.core.model.action_response",
        "qualname": "ActionResponse.DoesNotExist",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;class &#x27;neomodel.core.ActionResponseDoesNotExist&#x27;&gt;"
    }, {
        "fullname": "open_precision.core.model.course",
        "modulename": "open_precision.core.model.course",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.model.course.Course",
        "modulename": "open_precision.core.model.course",
        "qualname": "Course",
        "kind": "class",
        "doc": "<p>Base class for all node definitions to inherit from.</p>\n\n<p>If you want to create your own abstract classes set:\n    __abstract_node__ = True</p>\n",
        "bases": "neomodel.core.StructuredNode, open_precision.core.model.DataModelBase"
    }, {
        "fullname": "open_precision.core.model.course.Course.uuid",
        "modulename": "open_precision.core.model.course",
        "qualname": "Course.uuid",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": str",
        "default_value": "&lt;neomodel.properties.UniqueIdProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.course.Course.name",
        "modulename": "open_precision.core.model.course",
        "qualname": "Course.name",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": str",
        "default_value": "&lt;neomodel.properties.StringProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.course.Course.description",
        "modulename": "open_precision.core.model.course",
        "qualname": "Course.description",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": str",
        "default_value": "&lt;neomodel.properties.StringProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.course.Course.CONTAINS",
        "modulename": "open_precision.core.model.course",
        "qualname": "Course.CONTAINS",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": neomodel.relationship_manager.RelationshipTo",
        "default_value": "&lt;neomodel.relationship_manager.RelationshipTo object&gt;"
    }, {
        "fullname": "open_precision.core.model.course.Course.add_path",
        "modulename": "open_precision.core.model.course",
        "qualname": "Course.add_path",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">path</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">path</span><span class=\"o\">.</span><span class=\"n\">Path</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.course.Course.DoesNotExist",
        "modulename": "open_precision.core.model.course",
        "qualname": "Course.DoesNotExist",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;class &#x27;neomodel.core.CourseDoesNotExist&#x27;&gt;"
    }, {
        "fullname": "open_precision.core.model.data_subscription",
        "modulename": "open_precision.core.model.data_subscription",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.model.data_subscription.DataSubscription",
        "modulename": "open_precision.core.model.data_subscription",
        "qualname": "DataSubscription",
        "kind": "class",
        "doc": "<p></p>\n",
        "bases": "open_precision.core.model.DataModelBase"
    }, {
        "fullname": "open_precision.core.model.data_subscription.DataSubscription.__init__",
        "modulename": "open_precision.core.model.data_subscription",
        "qualname": "DataSubscription.__init__",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">func</span><span class=\"p\">:</span> <span class=\"n\">Optional</span><span class=\"p\">[</span><span class=\"n\">Callable</span><span class=\"p\">]</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">args</span><span class=\"p\">:</span> <span class=\"n\">Optional</span><span class=\"p\">[</span><span class=\"n\">Tuple</span><span class=\"p\">[</span><span class=\"n\">Any</span><span class=\"p\">,</span> <span class=\"o\">...</span><span class=\"p\">]]</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">kw_args</span><span class=\"p\">:</span> <span class=\"n\">Optional</span><span class=\"p\">[</span><span class=\"n\">Tuple</span><span class=\"p\">[</span><span class=\"n\">Tuple</span><span class=\"p\">[</span><span class=\"nb\">str</span><span class=\"p\">,</span> <span class=\"n\">Any</span><span class=\"p\">]]]</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">period_length</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">=</span> <span class=\"mi\">0</span></span>)</span>"
    }, {
        "fullname": "open_precision.core.model.data_subscription.DataSubscription.func",
        "modulename": "open_precision.core.model.data_subscription",
        "qualname": "DataSubscription.func",
        "kind": "variable",
        "doc": "<p>TODO when remodelling the data subscriptions to persist throughout system restarts, __hash__ must use a subset of \nfunc's properties (no session specific information, like place in memory).\nThis could be done by creating a new property, compute it from func in __post_init__ and set hash=False for func.</p>\n",
        "annotation": ": Optional[Callable]",
        "default_value": "None"
    }, {
        "fullname": "open_precision.core.model.data_subscription.DataSubscription.args",
        "modulename": "open_precision.core.model.data_subscription",
        "qualname": "DataSubscription.args",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": Optional[Tuple[Any, ...]]",
        "default_value": "None"
    }, {
        "fullname": "open_precision.core.model.data_subscription.DataSubscription.kw_args",
        "modulename": "open_precision.core.model.data_subscription",
        "qualname": "DataSubscription.kw_args",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": Optional[Tuple[Tuple[str, Any]]]",
        "default_value": "None"
    }, {
        "fullname": "open_precision.core.model.data_subscription.DataSubscription.period_length",
        "modulename": "open_precision.core.model.data_subscription",
        "qualname": "DataSubscription.period_length",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": int",
        "default_value": "0"
    }, {
        "fullname": "open_precision.core.model.data_subscription.DataSubscriptionProperty",
        "modulename": "open_precision.core.model.data_subscription",
        "qualname": "DataSubscriptionProperty",
        "kind": "class",
        "doc": "<p>Property for storing data in a Neo4j database using dill serialization.</p>\n",
        "bases": "open_precision.utils.neomodel.DillProperty[open_precision.core.model.data_subscription.DataSubscription], neomodel.properties.Property"
    }, {
        "fullname": "open_precision.core.model.data_subscription.DataSubscriptionSchema",
        "modulename": "open_precision.core.model.data_subscription",
        "qualname": "DataSubscriptionSchema",
        "kind": "class",
        "doc": "<p></p>\n",
        "bases": "pydantic.main.BaseModel"
    }, {
        "fullname": "open_precision.core.model.data_subscription.DataSubscriptionSchema.socket_id",
        "modulename": "open_precision.core.model.data_subscription",
        "qualname": "DataSubscriptionSchema.socket_id",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": str"
    }, {
        "fullname": "open_precision.core.model.data_subscription.DataSubscriptionSchema.period_length",
        "modulename": "open_precision.core.model.data_subscription",
        "qualname": "DataSubscriptionSchema.period_length",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": int"
    }, {
        "fullname": "open_precision.core.model.location",
        "modulename": "open_precision.core.model.location",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.model.location.Location",
        "modulename": "open_precision.core.model.location",
        "qualname": "Location",
        "kind": "class",
        "doc": "<p></p>\n",
        "bases": "open_precision.core.model.DataModelBase"
    }, {
        "fullname": "open_precision.core.model.location.Location.__init__",
        "modulename": "open_precision.core.model.location",
        "qualname": "Location.__init__",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">x</span><span class=\"p\">:</span> <span class=\"nb\">float</span> <span class=\"o\">=</span> <span class=\"mf\">0.0</span>,</span><span class=\"param\">\t<span class=\"n\">y</span><span class=\"p\">:</span> <span class=\"nb\">float</span> <span class=\"o\">=</span> <span class=\"mf\">0.0</span>,</span><span class=\"param\">\t<span class=\"n\">z</span><span class=\"p\">:</span> <span class=\"nb\">float</span> <span class=\"o\">=</span> <span class=\"mf\">0.0</span>,</span><span class=\"param\">\t<span class=\"n\">error</span><span class=\"p\">:</span> <span class=\"nb\">float</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span>)</span>"
    }, {
        "fullname": "open_precision.core.model.location.Location.x",
        "modulename": "open_precision.core.model.location",
        "qualname": "Location.x",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": float",
        "default_value": "0.0"
    }, {
        "fullname": "open_precision.core.model.location.Location.y",
        "modulename": "open_precision.core.model.location",
        "qualname": "Location.y",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": float",
        "default_value": "0.0"
    }, {
        "fullname": "open_precision.core.model.location.Location.z",
        "modulename": "open_precision.core.model.location",
        "qualname": "Location.z",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": float",
        "default_value": "0.0"
    }, {
        "fullname": "open_precision.core.model.location.Location.error",
        "modulename": "open_precision.core.model.location",
        "qualname": "Location.error",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": float | None",
        "default_value": "None"
    }, {
        "fullname": "open_precision.core.model.location.Location.is_valid",
        "modulename": "open_precision.core.model.location",
        "qualname": "Location.is_valid",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.location.Location.to_numpy",
        "modulename": "open_precision.core.model.location",
        "qualname": "Location.to_numpy",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">) -> <span class=\"o\">&lt;</span><span class=\"n\">built</span><span class=\"o\">-</span><span class=\"ow\">in</span> <span class=\"n\">function</span> <span class=\"n\">array</span><span class=\"o\">&gt;</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.location.LocationProperty",
        "modulename": "open_precision.core.model.location",
        "qualname": "LocationProperty",
        "kind": "class",
        "doc": "<p>A property that stores a Location object as a list of floats.</p>\n",
        "bases": "neomodel.properties.Property"
    }, {
        "fullname": "open_precision.core.model.location.LocationProperty.inflate",
        "modulename": "open_precision.core.model.location",
        "qualname": "LocationProperty.inflate",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">value</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">float</span><span class=\"p\">]</span></span><span class=\"return-annotation\">) -> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">location</span><span class=\"o\">.</span><span class=\"n\">Location</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.location.LocationProperty.deflate",
        "modulename": "open_precision.core.model.location",
        "qualname": "LocationProperty.deflate",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">value</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">location</span><span class=\"o\">.</span><span class=\"n\">Location</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.orientation",
        "modulename": "open_precision.core.model.orientation",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.model.orientation.Orientation",
        "modulename": "open_precision.core.model.orientation",
        "qualname": "Orientation",
        "kind": "class",
        "doc": "<p></p>\n",
        "bases": "pyquaternion.quaternion.Quaternion, open_precision.core.model.DataModelBase"
    }, {
        "fullname": "open_precision.core.model.orientation.Orientation.__init__",
        "modulename": "open_precision.core.model.orientation",
        "qualname": "Orientation.__init__",
        "kind": "function",
        "doc": "<p>Initialise a new Quaternion object.</p>\n\n<p>See Object Initialisation docs for complete behaviour:</p>\n\n<p><a href=\"https://kieranwynn.github.io/pyquaternion/#object-initialisation\">https://kieranwynn.github.io/pyquaternion/#object-initialisation</a></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"o\">*</span>, </span><span class=\"param\"><span class=\"n\">q</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span>)</span>"
    }, {
        "fullname": "open_precision.core.model.orientation.Orientation.q",
        "modulename": "open_precision.core.model.orientation",
        "qualname": "Orientation.q",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": numpy.ndarray",
        "default_value": "None"
    }, {
        "fullname": "open_precision.core.model.orientation.OrientationProperty",
        "modulename": "open_precision.core.model.orientation",
        "qualname": "OrientationProperty",
        "kind": "class",
        "doc": "<p>Property for storing Orientation objects in Neo4j\nOrientation Quaternion values are stored as a list of 4 floats.</p>\n",
        "bases": "neomodel.properties.Property"
    }, {
        "fullname": "open_precision.core.model.orientation.OrientationProperty.inflate",
        "modulename": "open_precision.core.model.orientation",
        "qualname": "OrientationProperty.inflate",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span>,</span><span class=\"param\">\t<span class=\"n\">value</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">float</span><span class=\"p\">]</span></span><span class=\"return-annotation\">) -> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">orientation</span><span class=\"o\">.</span><span class=\"n\">Orientation</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.orientation.OrientationProperty.deflate",
        "modulename": "open_precision.core.model.orientation",
        "qualname": "OrientationProperty.deflate",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span>,</span><span class=\"param\">\t<span class=\"n\">value</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">orientation</span><span class=\"o\">.</span><span class=\"n\">Orientation</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">float</span><span class=\"p\">]</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.path",
        "modulename": "open_precision.core.model.path",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.model.path.Path",
        "modulename": "open_precision.core.model.path",
        "qualname": "Path",
        "kind": "class",
        "doc": "<p>Base class for all node definitions to inherit from.</p>\n\n<p>If you want to create your own abstract classes set:\n    __abstract_node__ = True</p>\n",
        "bases": "neomodel.core.StructuredNode, open_precision.core.model.DataModelBase"
    }, {
        "fullname": "open_precision.core.model.path.Path.uuid",
        "modulename": "open_precision.core.model.path",
        "qualname": "Path.uuid",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": str",
        "default_value": "&lt;neomodel.properties.UniqueIdProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.path.Path.REQUIRES",
        "modulename": "open_precision.core.model.path",
        "qualname": "Path.REQUIRES",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": neomodel.relationship_manager.RelationshipTo",
        "default_value": "&lt;neomodel.relationship_manager.RelationshipTo object&gt;"
    }, {
        "fullname": "open_precision.core.model.path.Path.CONTAINS",
        "modulename": "open_precision.core.model.path",
        "qualname": "Path.CONTAINS",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": neomodel.relationship_manager.RelationshipTo",
        "default_value": "&lt;neomodel.relationship_manager.RelationshipTo object&gt;"
    }, {
        "fullname": "open_precision.core.model.path.Path.BEGINS_WITH",
        "modulename": "open_precision.core.model.path",
        "qualname": "Path.BEGINS_WITH",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": neomodel.relationship_manager.RelationshipFrom",
        "default_value": "&lt;neomodel.relationship_manager.RelationshipTo object&gt;"
    }, {
        "fullname": "open_precision.core.model.path.Path.ENDS_WITH",
        "modulename": "open_precision.core.model.path",
        "qualname": "Path.ENDS_WITH",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": neomodel.relationship_manager.RelationshipFrom",
        "default_value": "&lt;neomodel.relationship_manager.RelationshipTo object&gt;"
    }, {
        "fullname": "open_precision.core.model.path.Path.IS_CONTAINED_BY",
        "modulename": "open_precision.core.model.path",
        "qualname": "Path.IS_CONTAINED_BY",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": neomodel.relationship_manager.RelationshipFrom",
        "default_value": "&lt;neomodel.relationship_manager.RelationshipFrom object&gt;"
    }, {
        "fullname": "open_precision.core.model.path.Path.IS_REQUIRED_BY",
        "modulename": "open_precision.core.model.path",
        "qualname": "Path.IS_REQUIRED_BY",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": neomodel.relationship_manager.RelationshipFrom",
        "default_value": "&lt;neomodel.relationship_manager.RelationshipFrom object&gt;"
    }, {
        "fullname": "open_precision.core.model.path.Path.DoesNotExist",
        "modulename": "open_precision.core.model.path",
        "qualname": "Path.DoesNotExist",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;class &#x27;neomodel.core.PathDoesNotExist&#x27;&gt;"
    }, {
        "fullname": "open_precision.core.model.position",
        "modulename": "open_precision.core.model.position",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.model.position.Position",
        "modulename": "open_precision.core.model.position",
        "qualname": "Position",
        "kind": "class",
        "doc": "<p>A position consists of a location and an orientation.</p>\n",
        "bases": "open_precision.core.model.DataModelBase"
    }, {
        "fullname": "open_precision.core.model.position.Position.__init__",
        "modulename": "open_precision.core.model.position",
        "qualname": "Position.__init__",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"o\">*</span>,</span><span class=\"param\">\t<span class=\"n\">location</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">location</span><span class=\"o\">.</span><span class=\"n\">Location</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">orientation</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">orientation</span><span class=\"o\">.</span><span class=\"n\">Orientation</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span>)</span>"
    }, {
        "fullname": "open_precision.core.model.position.Position.location",
        "modulename": "open_precision.core.model.position",
        "qualname": "Position.location",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": open_precision.core.model.location.Location | None",
        "default_value": "None"
    }, {
        "fullname": "open_precision.core.model.position.Position.orientation",
        "modulename": "open_precision.core.model.position",
        "qualname": "Position.orientation",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": open_precision.core.model.orientation.Orientation | None",
        "default_value": "None"
    }, {
        "fullname": "open_precision.core.model.position.PositionProperty",
        "modulename": "open_precision.core.model.position",
        "qualname": "PositionProperty",
        "kind": "class",
        "doc": "<p>Property for storing Position objects in Neo4j.\nPosition values are stored as a list of 8 floats. The first 4 are the location, the last 4 are the orientation.</p>\n",
        "bases": "neomodel.properties.Property, open_precision.core.model.DataModelBase"
    }, {
        "fullname": "open_precision.core.model.position.PositionProperty.inflate",
        "modulename": "open_precision.core.model.position",
        "qualname": "PositionProperty.inflate",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">value</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">float</span><span class=\"p\">]</span></span><span class=\"return-annotation\">) -> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">position</span><span class=\"o\">.</span><span class=\"n\">Position</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.position.PositionProperty.deflate",
        "modulename": "open_precision.core.model.position",
        "qualname": "PositionProperty.deflate",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">value</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">position</span><span class=\"o\">.</span><span class=\"n\">Position</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">float</span><span class=\"p\">]</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.model.system_configuration",
        "modulename": "open_precision.core.model.system_configuration",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.model.system_configuration.SystemConfiguration",
        "modulename": "open_precision.core.model.system_configuration",
        "qualname": "SystemConfiguration",
        "kind": "class",
        "doc": "<p>TODO: implement usage, add to model mapping list\nA system configuration consists of a vehicle and a list of sensor.</p>\n",
        "bases": "open_precision.core.model.DataModelBase, neomodel.core.StructuredNode"
    }, {
        "fullname": "open_precision.core.model.system_configuration.SystemConfiguration.uuid",
        "modulename": "open_precision.core.model.system_configuration",
        "qualname": "SystemConfiguration.uuid",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": str",
        "default_value": "&lt;neomodel.properties.UniqueIdProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.system_configuration.SystemConfiguration.config",
        "modulename": "open_precision.core.model.system_configuration",
        "qualname": "SystemConfiguration.config",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": dict[str, str | list | dict]",
        "default_value": "&lt;neomodel.properties.JSONProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.system_configuration.SystemConfiguration.DoesNotExist",
        "modulename": "open_precision.core.model.system_configuration",
        "qualname": "SystemConfiguration.DoesNotExist",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;class &#x27;neomodel.core.SystemConfigurationDoesNotExist&#x27;&gt;"
    }, {
        "fullname": "open_precision.core.model.vehicle",
        "modulename": "open_precision.core.model.vehicle",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.model.vehicle.Vehicle",
        "modulename": "open_precision.core.model.vehicle",
        "qualname": "Vehicle",
        "kind": "class",
        "doc": "<p>Base class for all node definitions to inherit from.</p>\n\n<p>If you want to create your own abstract classes set:\n    __abstract_node__ = True</p>\n",
        "bases": "neomodel.core.StructuredNode, open_precision.core.model.DataModelBase"
    }, {
        "fullname": "open_precision.core.model.vehicle.Vehicle.name",
        "modulename": "open_precision.core.model.vehicle",
        "qualname": "Vehicle.name",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": str",
        "default_value": "&lt;neomodel.properties.StringProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.vehicle.Vehicle.turn_radius_left",
        "modulename": "open_precision.core.model.vehicle",
        "qualname": "Vehicle.turn_radius_left",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": float",
        "default_value": "&lt;neomodel.properties.FloatProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.vehicle.Vehicle.turn_radius_right",
        "modulename": "open_precision.core.model.vehicle",
        "qualname": "Vehicle.turn_radius_right",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": float",
        "default_value": "&lt;neomodel.properties.FloatProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.vehicle.Vehicle.wheelbase",
        "modulename": "open_precision.core.model.vehicle",
        "qualname": "Vehicle.wheelbase",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": float",
        "default_value": "&lt;neomodel.properties.FloatProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.vehicle.Vehicle.gps_receiver_offset",
        "modulename": "open_precision.core.model.vehicle",
        "qualname": "Vehicle.gps_receiver_offset",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": list[float]",
        "default_value": "&lt;neomodel.properties.ArrayProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.vehicle.Vehicle.DoesNotExist",
        "modulename": "open_precision.core.model.vehicle",
        "qualname": "Vehicle.DoesNotExist",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;class &#x27;neomodel.core.VehicleDoesNotExist&#x27;&gt;"
    }, {
        "fullname": "open_precision.core.model.vehicle_state",
        "modulename": "open_precision.core.model.vehicle_state",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.model.vehicle_state.VehicleState",
        "modulename": "open_precision.core.model.vehicle_state",
        "qualname": "VehicleState",
        "kind": "class",
        "doc": "<p>Base class for all node definitions to inherit from.</p>\n\n<p>If you want to create your own abstract classes set:\n    __abstract_node__ = True</p>\n",
        "bases": "neomodel.core.StructuredNode, open_precision.core.model.DataModelBase"
    }, {
        "fullname": "open_precision.core.model.vehicle_state.VehicleState.uuid",
        "modulename": "open_precision.core.model.vehicle_state",
        "qualname": "VehicleState.uuid",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": str",
        "default_value": "&lt;neomodel.properties.UniqueIdProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.vehicle_state.VehicleState.steering_angle",
        "modulename": "open_precision.core.model.vehicle_state",
        "qualname": "VehicleState.steering_angle",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": float | None",
        "default_value": "&lt;neomodel.properties.FloatProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.vehicle_state.VehicleState.speed",
        "modulename": "open_precision.core.model.vehicle_state",
        "qualname": "VehicleState.speed",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": float | None",
        "default_value": "&lt;neomodel.properties.FloatProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.vehicle_state.VehicleState.position",
        "modulename": "open_precision.core.model.vehicle_state",
        "qualname": "VehicleState.position",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": open_precision.core.model.position.Position | None",
        "default_value": "&lt;open_precision.core.model.position.PositionProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.vehicle_state.VehicleState.DoesNotExist",
        "modulename": "open_precision.core.model.vehicle_state",
        "qualname": "VehicleState.DoesNotExist",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;class &#x27;neomodel.core.VehicleStateDoesNotExist&#x27;&gt;"
    }, {
        "fullname": "open_precision.core.model.waypoint",
        "modulename": "open_precision.core.model.waypoint",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.model.waypoint.Waypoint",
        "modulename": "open_precision.core.model.waypoint",
        "qualname": "Waypoint",
        "kind": "class",
        "doc": "<p>Base class for all node definitions to inherit from.</p>\n\n<p>If you want to create your own abstract classes set:\n    __abstract_node__ = True</p>\n",
        "bases": "neomodel.core.StructuredNode, open_precision.core.model.DataModelBase"
    }, {
        "fullname": "open_precision.core.model.waypoint.Waypoint.uuid",
        "modulename": "open_precision.core.model.waypoint",
        "qualname": "Waypoint.uuid",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": str",
        "default_value": "&lt;neomodel.properties.UniqueIdProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.waypoint.Waypoint.location",
        "modulename": "open_precision.core.model.waypoint",
        "qualname": "Waypoint.location",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": open_precision.core.model.location.Location",
        "default_value": "&lt;open_precision.core.model.location.LocationProperty object&gt;"
    }, {
        "fullname": "open_precision.core.model.waypoint.Waypoint.PREDECESSOR",
        "modulename": "open_precision.core.model.waypoint",
        "qualname": "Waypoint.PREDECESSOR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": neomodel.relationship_manager.RelationshipFrom",
        "default_value": "&lt;neomodel.relationship_manager.RelationshipFrom object&gt;"
    }, {
        "fullname": "open_precision.core.model.waypoint.Waypoint.IS_CONTAINED_BY_PATH",
        "modulename": "open_precision.core.model.waypoint",
        "qualname": "Waypoint.IS_CONTAINED_BY_PATH",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": neomodel.relationship_manager.RelationshipFrom",
        "default_value": "&lt;neomodel.relationship_manager.RelationshipFrom object&gt;"
    }, {
        "fullname": "open_precision.core.model.waypoint.Waypoint.IS_CONTAINED_BY_COURSE",
        "modulename": "open_precision.core.model.waypoint",
        "qualname": "Waypoint.IS_CONTAINED_BY_COURSE",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": neomodel.relationship_manager.RelationshipFrom",
        "default_value": "&lt;neomodel.relationship_manager.RelationshipFrom object&gt;"
    }, {
        "fullname": "open_precision.core.model.waypoint.Waypoint.SUCCESSOR",
        "modulename": "open_precision.core.model.waypoint",
        "qualname": "Waypoint.SUCCESSOR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": neomodel.relationship_manager.RelationshipFrom",
        "default_value": "&lt;neomodel.relationship_manager.RelationshipFrom object&gt;"
    }, {
        "fullname": "open_precision.core.model.waypoint.Waypoint.DoesNotExist",
        "modulename": "open_precision.core.model.waypoint",
        "qualname": "Waypoint.DoesNotExist",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;class &#x27;neomodel.core.WaypointDoesNotExist&#x27;&gt;"
    }, {
        "fullname": "open_precision.core.plugin_base_classes",
        "modulename": "open_precision.core.plugin_base_classes",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.course_generator",
        "modulename": "open_precision.core.plugin_base_classes.course_generator",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.course_generator.CourseGenerator",
        "modulename": "open_precision.core.plugin_base_classes.course_generator",
        "qualname": "CourseGenerator",
        "kind": "class",
        "doc": "<p>Generates a Path and outputs next position based on position (and last actions)</p>\n",
        "bases": "open_precision.core.plugin_base_classes.plugin.Plugin, abc.ABC"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.course_generator.CourseGenerator.cleanup",
        "modulename": "open_precision.core.plugin_base_classes.course_generator",
        "qualname": "CourseGenerator.cleanup",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.course_generator.CourseGenerator.generate_course",
        "modulename": "open_precision.core.plugin_base_classes.course_generator",
        "qualname": "CourseGenerator.generate_course",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">) -> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">course</span><span class=\"o\">.</span><span class=\"n\">Course</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.navigator",
        "modulename": "open_precision.core.plugin_base_classes.navigator",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.navigator.Navigator",
        "modulename": "open_precision.core.plugin_base_classes.navigator",
        "qualname": "Navigator",
        "kind": "class",
        "doc": "<p>computes from current position and target point (or line) to output/call actions that need to be performed in\norder to the target point (or line)</p>\n",
        "bases": "open_precision.core.plugin_base_classes.plugin.Plugin, abc.ABC"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.navigator.Navigator.cleanup",
        "modulename": "open_precision.core.plugin_base_classes.navigator",
        "qualname": "Navigator.cleanup",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.navigator.Navigator.current_course",
        "modulename": "open_precision.core.plugin_base_classes.navigator",
        "qualname": "Navigator.current_course",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": open_precision.core.model.course.Course"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.navigator.Navigator.target_machine_state",
        "modulename": "open_precision.core.plugin_base_classes.navigator",
        "qualname": "Navigator.target_machine_state",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": open_precision.core.model.vehicle_state.VehicleState | None"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.navigator.Navigator.set_course_from_course_generator",
        "modulename": "open_precision.core.plugin_base_classes.navigator",
        "qualname": "Navigator.set_course_from_course_generator",
        "kind": "function",
        "doc": "<p>sets the course generator to the one with the given identifier,\npossible identifiers are: 'a_heading_parallel'</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">course_generator_identifier</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">=</span> <span class=\"s1\">&#39;a_heading_parallel&#39;</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.plugin",
        "modulename": "open_precision.core.plugin_base_classes.plugin",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.plugin.Plugin",
        "modulename": "open_precision.core.plugin_base_classes.plugin",
        "qualname": "Plugin",
        "kind": "class",
        "doc": "<p>Helper class that provides a standard way to create an ABC using\ninheritance.</p>\n",
        "bases": "abc.ABC"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.plugin.Plugin.cleanup",
        "modulename": "open_precision.core.plugin_base_classes.plugin",
        "qualname": "Plugin.cleanup",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor.AbsoluteOrientationSensor",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor",
        "qualname": "AbsoluteOrientationSensor",
        "kind": "class",
        "doc": "<p>Helper class that provides a standard way to create an ABC using\ninheritance.</p>\n",
        "bases": "open_precision.core.plugin_base_classes.plugin.Plugin, abc.ABC"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor.AbsoluteOrientationSensor.orientation",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor",
        "qualname": "AbsoluteOrientationSensor.orientation",
        "kind": "variable",
        "doc": "<p>returns an orientation quaternion</p>\n",
        "annotation": ": open_precision.core.model.orientation.Orientation | None"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor.AbsoluteOrientationSensor.gravity",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor",
        "qualname": "AbsoluteOrientationSensor.gravity",
        "kind": "variable",
        "doc": "<p>returns an gravity vector</p>\n",
        "annotation": ": numpy.ndarray | None"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.global_positioning_system",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.global_positioning_system",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.global_positioning_system.GlobalPositioningSystem",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.global_positioning_system",
        "qualname": "GlobalPositioningSystem",
        "kind": "class",
        "doc": "<p>Helper class that provides a standard way to create an ABC using\ninheritance.</p>\n",
        "bases": "open_precision.core.plugin_base_classes.plugin.Plugin, abc.ABC"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.global_positioning_system.GlobalPositioningSystem.location",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.global_positioning_system",
        "qualname": "GlobalPositioningSystem.location",
        "kind": "variable",
        "doc": "<p>returns a Location object</p>\n",
        "annotation": ": open_precision.core.model.location.Location | None"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.inertial_measurement_unit",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.inertial_measurement_unit",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.inertial_measurement_unit.InertialMeasurementUnit",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.inertial_measurement_unit",
        "qualname": "InertialMeasurementUnit",
        "kind": "class",
        "doc": "<p>Helper class that provides a standard way to create an ABC using\ninheritance.</p>\n",
        "bases": "open_precision.core.plugin_base_classes.plugin.Plugin, abc.ABC"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.inertial_measurement_unit.InertialMeasurementUnit.scaled_acceleration",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.inertial_measurement_unit",
        "qualname": "InertialMeasurementUnit.scaled_acceleration",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": numpy.ndarray | None"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.inertial_measurement_unit.InertialMeasurementUnit.scaled_angular_acceleration",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.inertial_measurement_unit",
        "qualname": "InertialMeasurementUnit.scaled_angular_acceleration",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": numpy.ndarray | None"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.inertial_measurement_unit.InertialMeasurementUnit.scaled_magnetometer",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.inertial_measurement_unit",
        "qualname": "InertialMeasurementUnit.scaled_magnetometer",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": numpy.ndarray | None"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater.WorldMagneticModelCalculator",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater",
        "qualname": "WorldMagneticModelCalculator",
        "kind": "class",
        "doc": "<p>Helper class that provides a standard way to create an ABC using\ninheritance.</p>\n",
        "bases": "open_precision.core.plugin_base_classes.plugin.Plugin, abc.ABC"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater.WorldMagneticModelCalculator.declination",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater",
        "qualname": "WorldMagneticModelCalculator.declination",
        "kind": "variable",
        "doc": "<p>returns the locational magnetic declination (magnetic variation) in degrees</p>\n",
        "annotation": ": float"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater.WorldMagneticModelCalculator.inclination",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater",
        "qualname": "WorldMagneticModelCalculator.inclination",
        "kind": "variable",
        "doc": "<p>returns the locational magnetic inclination in degrees</p>\n",
        "annotation": ": float"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater.WorldMagneticModelCalculator.total_intensity",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater",
        "qualname": "WorldMagneticModelCalculator.total_intensity",
        "kind": "variable",
        "doc": "<p>returns the total intensity in nT</p>\n",
        "annotation": ": float"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater.WorldMagneticModelCalculator.horizontal_intensity",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater",
        "qualname": "WorldMagneticModelCalculator.horizontal_intensity",
        "kind": "variable",
        "doc": "<p>returns the horizontal intensity in nT</p>\n",
        "annotation": ": float"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater.WorldMagneticModelCalculator.north_component",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater",
        "qualname": "WorldMagneticModelCalculator.north_component",
        "kind": "variable",
        "doc": "<p>returns the north (X) component in nT</p>\n",
        "annotation": ": float"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater.WorldMagneticModelCalculator.east_component",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater",
        "qualname": "WorldMagneticModelCalculator.east_component",
        "kind": "variable",
        "doc": "<p>returns the east (Y) component in nT</p>\n",
        "annotation": ": float"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater.WorldMagneticModelCalculator.vertical_component",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater",
        "qualname": "WorldMagneticModelCalculator.vertical_component",
        "kind": "variable",
        "doc": "<p>returns the vertical (Z) component in nT</p>\n",
        "annotation": ": float"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater.WorldMagneticModelCalculator.quaternion",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater",
        "qualname": "WorldMagneticModelCalculator.quaternion",
        "kind": "variable",
        "doc": "<p>returns the quaternion describing the rotation from north to the magnetic vector</p>\n",
        "annotation": ": float"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater.WorldMagneticModelCalculator.field_vector",
        "modulename": "open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater",
        "qualname": "WorldMagneticModelCalculator.field_vector",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": List[float]"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.vehicle_state_builder",
        "modulename": "open_precision.core.plugin_base_classes.vehicle_state_builder",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.vehicle_state_builder.VehicleStateBuilder",
        "modulename": "open_precision.core.plugin_base_classes.vehicle_state_builder",
        "qualname": "VehicleStateBuilder",
        "kind": "class",
        "doc": "<p>Helper class that provides a standard way to create an ABC using\ninheritance.</p>\n",
        "bases": "open_precision.core.plugin_base_classes.plugin.Plugin, abc.ABC"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.vehicle_state_builder.VehicleStateBuilder.cleanup",
        "modulename": "open_precision.core.plugin_base_classes.vehicle_state_builder",
        "qualname": "VehicleStateBuilder.cleanup",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.vehicle_state_builder.VehicleStateBuilder.vehicle_state",
        "modulename": "open_precision.core.plugin_base_classes.vehicle_state_builder",
        "qualname": "VehicleStateBuilder.vehicle_state",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": open_precision.core.model.vehicle_state.VehicleState | None"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.vehicle_state_builder.VehicleStateBuilder.current_position",
        "modulename": "open_precision.core.plugin_base_classes.vehicle_state_builder",
        "qualname": "VehicleStateBuilder.current_position",
        "kind": "variable",
        "doc": "<p>returns current position (location describes the location of the center of the rear axle)</p>\n",
        "annotation": ": open_precision.core.model.position.Position | None"
    }, {
        "fullname": "open_precision.core.plugin_base_classes.vehicle_state_builder.VehicleStateBuilder.is_ready",
        "modulename": "open_precision.core.plugin_base_classes.vehicle_state_builder",
        "qualname": "VehicleStateBuilder.is_ready",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": bool"
    }, {
        "fullname": "open_precision.external",
        "modulename": "open_precision.external",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver",
        "modulename": "open_precision.external.bno055_serial_driver",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_ADDRESS_A",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_ADDRESS_A",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "40"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_ADDRESS_B",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_ADDRESS_B",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "41"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_ID",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_ID",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "160"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_PAGE_ID_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_PAGE_ID_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "7"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_CHIP_ID_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_CHIP_ID_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "0"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_ACCEL_REV_ID_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_ACCEL_REV_ID_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "1"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_MAG_REV_ID_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_MAG_REV_ID_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "2"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_GYRO_REV_ID_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_GYRO_REV_ID_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "3"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SW_REV_ID_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SW_REV_ID_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "4"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SW_REV_ID_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SW_REV_ID_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "5"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_BL_REV_ID_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_BL_REV_ID_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "6"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_ACCEL_DATA_X_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_ACCEL_DATA_X_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "8"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_ACCEL_DATA_X_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_ACCEL_DATA_X_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "9"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_ACCEL_DATA_Y_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_ACCEL_DATA_Y_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "10"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_ACCEL_DATA_Y_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_ACCEL_DATA_Y_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "11"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_ACCEL_DATA_Z_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_ACCEL_DATA_Z_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "12"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_ACCEL_DATA_Z_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_ACCEL_DATA_Z_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "13"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_MAG_DATA_X_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_MAG_DATA_X_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "14"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_MAG_DATA_X_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_MAG_DATA_X_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "15"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_MAG_DATA_Y_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_MAG_DATA_Y_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "16"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_MAG_DATA_Y_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_MAG_DATA_Y_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "17"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_MAG_DATA_Z_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_MAG_DATA_Z_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "18"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_MAG_DATA_Z_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_MAG_DATA_Z_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "19"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_GYRO_DATA_X_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_GYRO_DATA_X_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "20"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_GYRO_DATA_X_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_GYRO_DATA_X_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "21"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_GYRO_DATA_Y_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_GYRO_DATA_Y_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "22"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_GYRO_DATA_Y_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_GYRO_DATA_Y_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "23"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_GYRO_DATA_Z_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_GYRO_DATA_Z_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "24"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_GYRO_DATA_Z_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_GYRO_DATA_Z_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "25"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_EULER_H_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_EULER_H_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "26"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_EULER_H_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_EULER_H_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "27"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_EULER_R_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_EULER_R_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "28"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_EULER_R_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_EULER_R_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "29"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_EULER_P_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_EULER_P_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "30"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_EULER_P_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_EULER_P_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "31"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_QUATERNION_DATA_W_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_QUATERNION_DATA_W_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "32"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_QUATERNION_DATA_W_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_QUATERNION_DATA_W_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "33"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_QUATERNION_DATA_X_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_QUATERNION_DATA_X_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "34"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_QUATERNION_DATA_X_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_QUATERNION_DATA_X_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "35"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_QUATERNION_DATA_Y_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_QUATERNION_DATA_Y_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "36"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_QUATERNION_DATA_Y_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_QUATERNION_DATA_Y_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "37"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_QUATERNION_DATA_Z_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_QUATERNION_DATA_Z_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "38"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_QUATERNION_DATA_Z_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_QUATERNION_DATA_Z_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "39"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_LINEAR_ACCEL_DATA_X_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_LINEAR_ACCEL_DATA_X_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "40"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_LINEAR_ACCEL_DATA_X_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_LINEAR_ACCEL_DATA_X_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "41"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_LINEAR_ACCEL_DATA_Y_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_LINEAR_ACCEL_DATA_Y_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "42"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_LINEAR_ACCEL_DATA_Y_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_LINEAR_ACCEL_DATA_Y_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "43"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_LINEAR_ACCEL_DATA_Z_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_LINEAR_ACCEL_DATA_Z_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "44"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_LINEAR_ACCEL_DATA_Z_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_LINEAR_ACCEL_DATA_Z_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "45"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_GRAVITY_DATA_X_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_GRAVITY_DATA_X_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "46"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_GRAVITY_DATA_X_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_GRAVITY_DATA_X_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "47"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_GRAVITY_DATA_Y_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_GRAVITY_DATA_Y_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "48"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_GRAVITY_DATA_Y_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_GRAVITY_DATA_Y_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "49"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_GRAVITY_DATA_Z_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_GRAVITY_DATA_Z_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "50"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_GRAVITY_DATA_Z_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_GRAVITY_DATA_Z_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "51"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_TEMP_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_TEMP_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "52"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_CALIB_STAT_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_CALIB_STAT_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "53"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SELFTEST_RESULT_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SELFTEST_RESULT_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "54"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_INTR_STAT_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_INTR_STAT_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "55"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SYS_CLK_STAT_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SYS_CLK_STAT_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "56"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SYS_STAT_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SYS_STAT_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "57"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SYS_ERR_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SYS_ERR_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "58"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_UNIT_SEL_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_UNIT_SEL_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "59"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_DATA_SELECT_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_DATA_SELECT_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "60"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_OPR_MODE_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_OPR_MODE_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "61"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_PWR_MODE_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_PWR_MODE_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "62"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SYS_TRIGGER_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SYS_TRIGGER_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "63"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_TEMP_SOURCE_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_TEMP_SOURCE_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "64"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_AXIS_MAP_CONFIG_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_AXIS_MAP_CONFIG_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "65"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_AXIS_MAP_SIGN_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_AXIS_MAP_SIGN_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "66"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.AXIS_REMAP_X",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "AXIS_REMAP_X",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "0"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.AXIS_REMAP_Y",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "AXIS_REMAP_Y",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "1"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.AXIS_REMAP_Z",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "AXIS_REMAP_Z",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "2"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.AXIS_REMAP_POSITIVE",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "AXIS_REMAP_POSITIVE",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "0"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.AXIS_REMAP_NEGATIVE",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "AXIS_REMAP_NEGATIVE",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "1"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_0_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_0_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "67"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_0_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_0_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "68"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_1_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_1_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "69"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_1_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_1_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "70"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_2_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_2_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "71"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_2_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_2_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "72"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_3_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_3_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "73"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_3_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_3_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "74"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_4_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_4_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "75"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_4_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_4_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "76"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_5_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_5_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "77"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_5_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_5_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "78"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_6_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_6_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "79"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_6_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_6_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "80"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_7_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_7_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "81"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_7_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_7_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "82"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_8_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_8_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "83"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055_SIC_MATRIX_8_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055_SIC_MATRIX_8_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "84"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.ACCEL_OFFSET_X_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "ACCEL_OFFSET_X_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "85"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.ACCEL_OFFSET_X_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "ACCEL_OFFSET_X_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "86"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.ACCEL_OFFSET_Y_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "ACCEL_OFFSET_Y_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "87"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.ACCEL_OFFSET_Y_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "ACCEL_OFFSET_Y_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "88"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.ACCEL_OFFSET_Z_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "ACCEL_OFFSET_Z_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "89"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.ACCEL_OFFSET_Z_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "ACCEL_OFFSET_Z_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "90"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.MAG_OFFSET_X_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "MAG_OFFSET_X_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "91"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.MAG_OFFSET_X_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "MAG_OFFSET_X_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "92"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.MAG_OFFSET_Y_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "MAG_OFFSET_Y_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "93"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.MAG_OFFSET_Y_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "MAG_OFFSET_Y_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "94"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.MAG_OFFSET_Z_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "MAG_OFFSET_Z_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "95"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.MAG_OFFSET_Z_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "MAG_OFFSET_Z_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "96"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.GYRO_OFFSET_X_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "GYRO_OFFSET_X_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "97"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.GYRO_OFFSET_X_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "GYRO_OFFSET_X_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "98"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.GYRO_OFFSET_Y_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "GYRO_OFFSET_Y_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "99"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.GYRO_OFFSET_Y_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "GYRO_OFFSET_Y_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "100"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.GYRO_OFFSET_Z_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "GYRO_OFFSET_Z_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "101"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.GYRO_OFFSET_Z_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "GYRO_OFFSET_Z_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "102"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.ACCEL_RADIUS_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "ACCEL_RADIUS_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "103"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.ACCEL_RADIUS_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "ACCEL_RADIUS_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "104"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.MAG_RADIUS_LSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "MAG_RADIUS_LSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "105"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.MAG_RADIUS_MSB_ADDR",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "MAG_RADIUS_MSB_ADDR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "106"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.POWER_MODE_NORMAL",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "POWER_MODE_NORMAL",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "0"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.POWER_MODE_LOWPOWER",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "POWER_MODE_LOWPOWER",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "1"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.POWER_MODE_SUSPEND",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "POWER_MODE_SUSPEND",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "2"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.OPERATION_MODE_CONFIG",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "OPERATION_MODE_CONFIG",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "0"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.OPERATION_MODE_ACCONLY",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "OPERATION_MODE_ACCONLY",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "1"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.OPERATION_MODE_MAGONLY",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "OPERATION_MODE_MAGONLY",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "2"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.OPERATION_MODE_GYRONLY",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "OPERATION_MODE_GYRONLY",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "3"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.OPERATION_MODE_ACCMAG",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "OPERATION_MODE_ACCMAG",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "4"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.OPERATION_MODE_ACCGYRO",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "OPERATION_MODE_ACCGYRO",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "5"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.OPERATION_MODE_MAGGYRO",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "OPERATION_MODE_MAGGYRO",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "6"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.OPERATION_MODE_AMG",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "OPERATION_MODE_AMG",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "7"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.OPERATION_MODE_IMUPLUS",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "OPERATION_MODE_IMUPLUS",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "8"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.OPERATION_MODE_COMPASS",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "OPERATION_MODE_COMPASS",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "9"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.OPERATION_MODE_M4G",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "OPERATION_MODE_M4G",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "10"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.OPERATION_MODE_NDOF_FMC_OFF",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "OPERATION_MODE_NDOF_FMC_OFF",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "11"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.OPERATION_MODE_NDOF",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "OPERATION_MODE_NDOF",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "12"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.logger",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "logger",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&lt;Logger open_precision.external.bno055_serial_driver (WARNING)&gt;"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055",
        "kind": "class",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.__init__",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.__init__",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">serial_port</span><span class=\"o\">=</span><span class=\"kc\">None</span>, </span><span class=\"param\"><span class=\"n\">serial_timeout_sec</span><span class=\"o\">=</span><span class=\"mi\">5</span></span>)</span>"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.begin",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.begin",
        "kind": "function",
        "doc": "<p>Initialize the BNO055 sensor.  Must be called once before any other\nBNO055 library functions.  Will return True if the BNO055 was\nsuccessfully initialized, and False otherwise.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">mode</span><span class=\"o\">=</span><span class=\"mi\">12</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.set_mode",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.set_mode",
        "kind": "function",
        "doc": "<p>Set operation mode for BNO055 sensor.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">mode</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.get_revision",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.get_revision",
        "kind": "function",
        "doc": "<p>Return a tuple with revision information about the BNO055 chip.  Will\nreturn 5 values:</p>\n\n<ul>\n<li>Software revision</li>\n<li>Bootloader version</li>\n<li>Accelerometer ID</li>\n<li>Magnetometer ID</li>\n<li>Gyro ID</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.set_external_crystal",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.set_external_crystal",
        "kind": "function",
        "doc": "<p>Set if an external crystal is being used by passing True, otherwise\nuse the internal oscillator by passing False (the default behavior).</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">external_crystal</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.get_system_status",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.get_system_status",
        "kind": "function",
        "doc": "<p>Return a tuple with status information.  Three values will be returned:</p>\n\n<ul>\n<li>System status register value with the following meaning:\n0 = Idle\n1 = System Error\n2 = Initializing Peripherals\n3 = System Initialization\n4 = Executing Self-Test\n5 = Sensor fusion algorithm running\n6 = System running without fusion algorithms</li>\n<li>Self test result register value with the following meaning:\nBit value: 1 = test passed, 0 = test failed\nBit 0 = Accelerometer self test\nBit 1 = Magnetometer self test\nBit 2 = Gyroscope self test\nBit 3 = MCU self test\nValue of 0x0F = all good!</li>\n<li>System error register value with the following meaning:\n 0 = No error\n 1 = Peripheral initialization error\n 2 = System initialization error\n 3 = Self test result failed\n 4 = Register map value out of range\n 5 = Register map address out of range\n 6 = Register map write error\n 7 = BNO low power mode not available for selected operation mode\n 8 = Accelerometer power mode not available\n 9 = Fusion algorithm configuration error\n10 = Sensor configuration error</li>\n</ul>\n\n<p>If run_self_test is passed in as False then no self test is performed and\nNone will be returned for the self test result.  Note that running a\nself test requires going into config mode which will stop the fusion\nengine from running.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">run_self_test</span><span class=\"o\">=</span><span class=\"kc\">True</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.get_calibration_status",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.get_calibration_status",
        "kind": "function",
        "doc": "<p>Read the calibration status of the sensors and return a 4 tuple with\ncalibration status as follows:</p>\n\n<ul>\n<li>System, 3=fully calibrated, 0=not calibrated</li>\n<li>Gyroscope, 3=fully calibrated, 0=not calibrated</li>\n<li>Accelerometer, 3=fully calibrated, 0=not calibrated</li>\n<li>Magnetometer, 3=fully calibrated, 0=not calibrated</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.get_calibration",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.get_calibration",
        "kind": "function",
        "doc": "<p>Return the sensor's calibration data and return it as an array of\n22 bytes. Can be saved and then reloaded with the set_calibration function\nto quickly calibrate from a previously calculated set of calibration data.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.set_calibration",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.set_calibration",
        "kind": "function",
        "doc": "<p>Set the sensor's calibration data using a list of 22 bytes that\nrepresent the sensor offsets and calibration data.  This data should be\na value that was previously retrieved with get_calibration (and then\nperhaps persisted to disk or other location until needed again).</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">data</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.get_axis_remap",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.get_axis_remap",
        "kind": "function",
        "doc": "<p>Return a tuple with the axis remap register values.  This will return\n6 values with the following meaning:</p>\n\n<ul>\n<li>X axis remap (a value of AXIS_REMAP_X, AXIS_REMAP_Y, or AXIS_REMAP_Z.\nwhich indicates that the physical X axis of the chip\nis remapped to a different axis)</li>\n<li>Y axis remap (see above)</li>\n<li>Z axis remap (see above)</li>\n<li>X axis sign (a value of AXIS_REMAP_POSITIVE or AXIS_REMAP_NEGATIVE\nwhich indicates if the X axis values should be positive/\nnormal or negative/inverted.  The default is positive.)</li>\n<li>Y axis sign (see above)</li>\n<li>Z axis sign (see above)</li>\n</ul>\n\n<p>Note that by default the axis orientation of the BNO chip looks like\nthe following (taken from section 3.4, page 24 of the datasheet).  Notice\nthe dot in the corner that corresponds to the dot on the BNO chip:</p>\n\n<pre><code>               | Z axis\n               |\n               |   / X axis\n           ____|__/____\n</code></pre>\n\n<p>Y axis     / *   | /    /|\n  _________ /______|/    //\n           /___________ //\n          |____________|/</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.set_axis_remap",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.set_axis_remap",
        "kind": "function",
        "doc": "<p>Set axis remap for each axis.  The x, y, z parameter values should\nbe set to one of AXIS_REMAP_X, AXIS_REMAP_Y, or AXIS_REMAP_Z and will\nchange the BNO's axis to represent another axis.  Note that two axises\ncannot be mapped to the same axis, so the x, y, z params should be a\nunique combination of AXIS_REMAP_X, AXIS_REMAP_Y, AXIS_REMAP_Z values.</p>\n\n<p>The x_sign, y_sign, z_sign values represent if the axis should be positive\nor negative (inverted).</p>\n\n<p>See the get_axis_remap documentation for information on the orientation\nof the axises on the chip, and consult section 3.4 of the datasheet.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">x</span>, </span><span class=\"param\"><span class=\"n\">y</span>, </span><span class=\"param\"><span class=\"n\">z</span>, </span><span class=\"param\"><span class=\"n\">x_sign</span><span class=\"o\">=</span><span class=\"mi\">0</span>, </span><span class=\"param\"><span class=\"n\">y_sign</span><span class=\"o\">=</span><span class=\"mi\">0</span>, </span><span class=\"param\"><span class=\"n\">z_sign</span><span class=\"o\">=</span><span class=\"mi\">0</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.read_euler",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.read_euler",
        "kind": "function",
        "doc": "<p>Return the current absolute orientation as a tuple of heading, roll,\nand pitch euler angles in degrees.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.read_magnetometer",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.read_magnetometer",
        "kind": "function",
        "doc": "<p>Return the current magnetometer reading as a tuple of X, Y, Z values\nin micro-Teslas.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.read_gyroscope",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.read_gyroscope",
        "kind": "function",
        "doc": "<p>Return the current gyroscope (angular velocity) reading as a tuple of\nX, Y, Z values in degrees per second.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.read_accelerometer",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.read_accelerometer",
        "kind": "function",
        "doc": "<p>Return the current accelerometer reading as a tuple of X, Y, Z values\nin meters/second^2.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.read_linear_acceleration",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.read_linear_acceleration",
        "kind": "function",
        "doc": "<p>Return the current linear acceleration (acceleration from movement,\nnot from gravity) reading as a tuple of X, Y, Z values in meters/second^2.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.read_gravity",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.read_gravity",
        "kind": "function",
        "doc": "<p>Return the current gravity acceleration reading as a tuple of X, Y, Z\nvalues in meters/second^2.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.read_quaternion",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.read_quaternion",
        "kind": "function",
        "doc": "<p>Return the current orientation as a tuple of X, Y, Z, W quaternion\nvalues.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.external.bno055_serial_driver.BNO055.read_temp",
        "modulename": "open_precision.external.bno055_serial_driver",
        "qualname": "BNO055.read_temp",
        "kind": "function",
        "doc": "<p>Return the current temperature in Celsius.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers",
        "modulename": "open_precision.managers",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.managers.config_manager",
        "modulename": "open_precision.managers.config_manager",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.managers.config_manager.ConfigManager",
        "modulename": "open_precision.managers.config_manager",
        "qualname": "ConfigManager",
        "kind": "class",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.managers.config_manager.ConfigManager.__init__",
        "modulename": "open_precision.managers.config_manager",
        "qualname": "ConfigManager.__init__",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">manager</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">system_hub</span><span class=\"o\">.</span><span class=\"n\">SystemHub</span></span>)</span>"
    }, {
        "fullname": "open_precision.managers.config_manager.ConfigManager.register_value",
        "modulename": "open_precision.managers.config_manager",
        "qualname": "ConfigManager.register_value",
        "kind": "function",
        "doc": "<p>adds key/value pair to object's config if not already set</p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span>,</span><span class=\"param\">\t<span class=\"n\">origin_object</span><span class=\"p\">:</span> <span class=\"nb\">object</span>,</span><span class=\"param\">\t<span class=\"n\">key</span><span class=\"p\">:</span> <span class=\"nb\">str</span>,</span><span class=\"param\">\t<span class=\"n\">value</span><span class=\"p\">:</span> <span class=\"o\">&lt;</span><span class=\"n\">built</span><span class=\"o\">-</span><span class=\"ow\">in</span> <span class=\"n\">function</span> <span class=\"nb\">any</span><span class=\"o\">&gt;</span></span><span class=\"return-annotation\">) -> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">managers</span><span class=\"o\">.</span><span class=\"n\">config_manager</span><span class=\"o\">.</span><span class=\"n\">ConfigManager</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers.config_manager.ConfigManager.set_value",
        "modulename": "open_precision.managers.config_manager",
        "qualname": "ConfigManager.set_value",
        "kind": "function",
        "doc": "<p>updates key's value in object's config</p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span>,</span><span class=\"param\">\t<span class=\"n\">origin_object</span><span class=\"p\">:</span> <span class=\"nb\">object</span>,</span><span class=\"param\">\t<span class=\"n\">key</span><span class=\"p\">:</span> <span class=\"nb\">str</span>,</span><span class=\"param\">\t<span class=\"n\">value</span><span class=\"p\">:</span> <span class=\"o\">&lt;</span><span class=\"n\">built</span><span class=\"o\">-</span><span class=\"ow\">in</span> <span class=\"n\">function</span> <span class=\"nb\">any</span><span class=\"o\">&gt;</span></span><span class=\"return-annotation\">) -> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">managers</span><span class=\"o\">.</span><span class=\"n\">config_manager</span><span class=\"o\">.</span><span class=\"n\">ConfigManager</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers.config_manager.ConfigManager.get_value",
        "modulename": "open_precision.managers.config_manager",
        "qualname": "ConfigManager.get_value",
        "kind": "function",
        "doc": "<p>returns value of key from origin_object's config</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">origin_object</span><span class=\"p\">:</span> <span class=\"nb\">object</span>, </span><span class=\"param\"><span class=\"n\">key</span><span class=\"p\">:</span> <span class=\"nb\">str</span></span><span class=\"return-annotation\">) -> <span class=\"o\">&lt;</span><span class=\"n\">built</span><span class=\"o\">-</span><span class=\"ow\">in</span> <span class=\"n\">function</span> <span class=\"nb\">any</span><span class=\"o\">&gt;</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers.config_manager.ConfigManager.cleanup",
        "modulename": "open_precision.managers.config_manager",
        "qualname": "ConfigManager.cleanup",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers.config_manager.ConfigManager.load_config",
        "modulename": "open_precision.managers.config_manager",
        "qualname": "ConfigManager.load_config",
        "kind": "function",
        "doc": "<p>loads config file from yaml string or file</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>reload</strong>:  reinitializing backend after loading config if this is set to True</li>\n<li><strong>yaml</strong>:  if None, loads from file, else loads from this parameter (should be the yaml string)</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>None</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">yaml</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>, </span><span class=\"param\"><span class=\"n\">reload</span><span class=\"p\">:</span> <span class=\"nb\">bool</span> <span class=\"o\">=</span> <span class=\"kc\">False</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers.config_manager.ConfigManager.save_config_file",
        "modulename": "open_precision.managers.config_manager",
        "qualname": "ConfigManager.save_config_file",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers.config_manager.ConfigManager.get_config_string",
        "modulename": "open_precision.managers.config_manager",
        "qualname": "ConfigManager.get_config_string",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">str</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers.data_manager",
        "modulename": "open_precision.managers.data_manager",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.managers.data_manager.DataManager",
        "modulename": "open_precision.managers.data_manager",
        "qualname": "DataManager",
        "kind": "class",
        "doc": "<p>The DataManager manages data subscriptions and data updates. The goal is to bundle periodic api calls to reduce\ncomputational expenses and network traffic, as well as to move data update work to the server side. These periodic\ntasks either check for new data or are otherwise required to be called periodically.</p>\n\n<p>Concretely, equivalent system tasks are grouped, then called once if required by the schedule, then multicasted to\nthe specified clients via socketio. This is done by the open_precision.api.utils.engine_endpoint decorator, which\nalso contains more documentation on how data subscriptions work.</p>\n"
    }, {
        "fullname": "open_precision.managers.data_manager.DataManager.__init__",
        "modulename": "open_precision.managers.data_manager",
        "qualname": "DataManager.__init__",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">manager</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">system_hub</span><span class=\"o\">.</span><span class=\"n\">SystemHub</span></span>)</span>"
    }, {
        "fullname": "open_precision.managers.data_manager.DataManager.endpoint_dict",
        "modulename": "open_precision.managers.data_manager",
        "qualname": "DataManager.endpoint_dict",
        "kind": "variable",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.managers.data_manager.DataManager.inner_on_connect",
        "modulename": "open_precision.managers.data_manager",
        "qualname": "DataManager.inner_on_connect",
        "kind": "function",
        "doc": "<p>This func is called by the socketio server when a new client connects. It is not intended to be called from\noutside the system update loop.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>sid</strong>: </li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">sid</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers.data_manager.DataManager.inner_on_disconnect",
        "modulename": "open_precision.managers.data_manager",
        "qualname": "DataManager.inner_on_disconnect",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">sid</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers.data_manager.DataManager.do_update",
        "modulename": "open_precision.managers.data_manager",
        "qualname": "DataManager.do_update",
        "kind": "function",
        "doc": "<p>This func is called by the SystemHub to trigger a data update. It is not intended to be called from outside\nthe system update loop. It recomputes out of date data subscriptions and sends an update to subscribers if the\nvalue has changed.</p>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>None</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.managers.data_manager.DataManager.emit_error",
        "modulename": "open_precision.managers.data_manager",
        "qualname": "DataManager.emit_error",
        "kind": "function",
        "doc": "<p>emit an error in the error room</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">e</span><span class=\"p\">:</span> <span class=\"ne\">Exception</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.managers.data_manager.DataManager.add_data_subscription",
        "modulename": "open_precision.managers.data_manager",
        "qualname": "DataManager.add_data_subscription",
        "kind": "function",
        "doc": "<p>subscribe a socket id to a data subscription</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>sid</strong>: </li>\n<li><strong>data_subscription</strong>: </li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span>,</span><span class=\"param\">\t<span class=\"n\">sid</span><span class=\"p\">:</span> <span class=\"nb\">str</span>,</span><span class=\"param\">\t<span class=\"n\">data_subscription</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">data_subscription</span><span class=\"o\">.</span><span class=\"n\">DataSubscription</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers.data_manager.DataManager.remove_data_subscription",
        "modulename": "open_precision.managers.data_manager",
        "qualname": "DataManager.remove_data_subscription",
        "kind": "function",
        "doc": "<p>remove a data subscription for a given socket id and data subscription</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>sid</strong>: </li>\n<li><strong>data_subscription</strong>: </li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span>,</span><span class=\"param\">\t<span class=\"n\">sid</span><span class=\"p\">:</span> <span class=\"nb\">str</span>,</span><span class=\"param\">\t<span class=\"n\">data_subscription</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">data_subscription</span><span class=\"o\">.</span><span class=\"n\">DataSubscription</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers.data_manager.DataManager.remove_all_data_subscriptions",
        "modulename": "open_precision.managers.data_manager",
        "qualname": "DataManager.remove_all_data_subscriptions",
        "kind": "function",
        "doc": "<p>remove all data subscriptions for a given socket id</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>sid</strong>: </li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">sid</span><span class=\"p\">:</span> <span class=\"nb\">str</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers.data_manager.DataManager.get_exec_times",
        "modulename": "open_precision.managers.data_manager",
        "qualname": "DataManager.get_exec_times",
        "kind": "function",
        "doc": "<p>get the average execution times of all data subscriptions</p>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>dict[DataSubscription, float | None]</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span></span><span class=\"return-annotation\">) -> <span class=\"n\">Dict</span><span class=\"p\">[</span><span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">data_subscription</span><span class=\"o\">.</span><span class=\"n\">DataSubscription</span><span class=\"p\">,</span> <span class=\"nb\">float</span> <span class=\"o\">|</span> <span class=\"kc\">None</span><span class=\"p\">]</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers.plugin_manager",
        "modulename": "open_precision.managers.plugin_manager",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.managers.plugin_manager.get_classes_in_package",
        "modulename": "open_precision.managers.plugin_manager",
        "qualname": "get_classes_in_package",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">package</span>, </span><span class=\"param\"><span class=\"n\">classes</span><span class=\"p\">:</span> <span class=\"nb\">list</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">list</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers.plugin_manager.PluginManager",
        "modulename": "open_precision.managers.plugin_manager",
        "qualname": "PluginManager",
        "kind": "class",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.managers.plugin_manager.PluginManager.__init__",
        "modulename": "open_precision.managers.plugin_manager",
        "qualname": "PluginManager.__init__",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">manager</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">system_hub</span><span class=\"o\">.</span><span class=\"n\">SystemHub</span>,</span><span class=\"param\">\t<span class=\"n\">plugin_type_class</span><span class=\"p\">:</span> <span class=\"nb\">type</span>,</span><span class=\"param\">\t<span class=\"n\">plugin_package</span><span class=\"p\">:</span> <span class=\"nb\">str</span></span>)</span>"
    }, {
        "fullname": "open_precision.managers.plugin_manager.PluginManager.instance",
        "modulename": "open_precision.managers.plugin_manager",
        "qualname": "PluginManager.instance",
        "kind": "variable",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.managers.plugin_manager.PluginManager.plugin_type_class",
        "modulename": "open_precision.managers.plugin_manager",
        "qualname": "PluginManager.plugin_type_class",
        "kind": "variable",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.managers.system_task_manager",
        "modulename": "open_precision.managers.system_task_manager",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.managers.system_task_manager.SystemTaskManager",
        "modulename": "open_precision.managers.system_task_manager",
        "qualname": "SystemTaskManager",
        "kind": "class",
        "doc": "<p>This class is used to queue and handle system tasks (func calls) to be executed in the main thread.</p>\n\n<h2 id=\"implementation-details\">Implementation details:</h2>\n\n<p>queue_system_task(func, <em>args, *</em>kwargs) queues a system task (func call) to be executed in the main thread. The\npassed func, args, kwargs, and the pipe end for sending the result put in a shared queue. When calling\nhandle_tasks(amount) the given amount of tasks will be taken from the queue and executed in the main thread. The\nresult will then be sent back through the pipe. Which triggers the queue_system_task func to return the result\nto its caller.</p>\n"
    }, {
        "fullname": "open_precision.managers.system_task_manager.SystemTaskManager.__init__",
        "modulename": "open_precision.managers.system_task_manager",
        "qualname": "SystemTaskManager.__init__",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">manager</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">system_hub</span><span class=\"o\">.</span><span class=\"n\">SystemHub</span></span>)</span>"
    }, {
        "fullname": "open_precision.managers.system_task_manager.SystemTaskManager.task_queue",
        "modulename": "open_precision.managers.system_task_manager",
        "qualname": "SystemTaskManager.task_queue",
        "kind": "variable",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.managers.system_task_manager.SystemTaskManager.queue_system_task",
        "modulename": "open_precision.managers.system_task_manager",
        "qualname": "SystemTaskManager.queue_system_task",
        "kind": "function",
        "doc": "<p>Queues a system task (func call) to be executed in the main thread.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>func</strong>:  func to be executed, must take a SystemHub as first argument, all other arguments must be\npassed as args and kwargs</li>\n<li><strong>args</strong>:  positional arguments to be passed to func, must be serializable (dill)</li>\n<li><strong>kwargs</strong>:  keyword arguments to be passed to func, must be serializable (dill)</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>result of func</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span>,</span><span class=\"param\">\t<span class=\"n\">func</span><span class=\"p\">:</span> <span class=\"n\">Callable</span><span class=\"p\">[[</span><span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">system_hub</span><span class=\"o\">.</span><span class=\"n\">SystemHub</span><span class=\"p\">],</span> <span class=\"n\">Any</span><span class=\"p\">]</span>,</span><span class=\"param\">\t<span class=\"o\">*</span><span class=\"n\">args</span>,</span><span class=\"param\">\t<span class=\"o\">**</span><span class=\"n\">kwargs</span></span><span class=\"return-annotation\">) -> <span class=\"n\">Any</span>:</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.managers.system_task_manager.SystemTaskManager.handle_tasks",
        "modulename": "open_precision.managers.system_task_manager",
        "qualname": "SystemTaskManager.handle_tasks",
        "kind": "function",
        "doc": "<p>Executes the passed amount of tasks from the queue.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>amount</strong>:  amount of tasks to execute;\nIf amount is -1, tasks will be executed until the queue is empty. (default)\nIf amount is 0, all currently queued tasks will be executed. (not the same as -1)\nOtherwise, the passed amount of tasks will be executed.</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>None</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">amount</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">=</span> <span class=\"o\">-</span><span class=\"mi\">1</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.managers.vehicle_manager",
        "modulename": "open_precision.managers.vehicle_manager",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.managers.vehicle_manager.VehicleManager",
        "modulename": "open_precision.managers.vehicle_manager",
        "qualname": "VehicleManager",
        "kind": "class",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.managers.vehicle_manager.VehicleManager.__init__",
        "modulename": "open_precision.managers.vehicle_manager",
        "qualname": "VehicleManager.__init__",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">manager</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">system_hub</span><span class=\"o\">.</span><span class=\"n\">SystemHub</span></span>)</span>"
    }, {
        "fullname": "open_precision.managers.vehicle_manager.VehicleManager.cleanup",
        "modulename": "open_precision.managers.vehicle_manager",
        "qualname": "VehicleManager.cleanup",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers.vehicle_manager.VehicleManager.load_data",
        "modulename": "open_precision.managers.vehicle_manager",
        "qualname": "VehicleManager.load_data",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers.vehicle_manager.VehicleManager.save_data",
        "modulename": "open_precision.managers.vehicle_manager",
        "qualname": "VehicleManager.save_data",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.managers.vehicle_manager.VehicleManager.current_vehicle",
        "modulename": "open_precision.managers.vehicle_manager",
        "qualname": "VehicleManager.current_vehicle",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": open_precision.core.model.vehicle.Vehicle"
    }, {
        "fullname": "open_precision.managers.vehicle_manager.VehicleManager.vehicles",
        "modulename": "open_precision.managers.vehicle_manager",
        "qualname": "VehicleManager.vehicles",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": list[open_precision.core.model.vehicle.Vehicle]"
    }, {
        "fullname": "open_precision.system_hub",
        "modulename": "open_precision.system_hub",
        "kind": "module",
        "doc": "<p>This file contains the SystemHub class, which is the central backbone of every instance of the application.</p>\n"
    }, {
        "fullname": "open_precision.system_hub.SystemHub",
        "modulename": "open_precision.system_hub",
        "qualname": "SystemHub",
        "kind": "class",
        "doc": "<p>reponsible for dependency injection, instance management, starting, reloading and stopping the system</p>\n"
    }, {
        "fullname": "open_precision.system_hub.SystemHub.start_update_loop",
        "modulename": "open_precision.system_hub",
        "qualname": "SystemHub.start_update_loop",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.system_hub.SystemHub.stop_update_loop",
        "modulename": "open_precision.system_hub",
        "qualname": "SystemHub.stop_update_loop",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.system_hub.SystemHub.stop",
        "modulename": "open_precision.system_hub",
        "qualname": "SystemHub.stop",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "async def"
    }, {
        "fullname": "open_precision.system_hub.SystemHub.config",
        "modulename": "open_precision.system_hub",
        "qualname": "SystemHub.config",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": open_precision.managers.config_manager.ConfigManager"
    }, {
        "fullname": "open_precision.system_hub.SystemHub.vehicles",
        "modulename": "open_precision.system_hub",
        "qualname": "SystemHub.vehicles",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": open_precision.managers.vehicle_manager.VehicleManager"
    }, {
        "fullname": "open_precision.system_hub.SystemHub.plugins",
        "modulename": "open_precision.system_hub",
        "qualname": "SystemHub.plugins",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": dict[object, any]"
    }, {
        "fullname": "open_precision.system_hub.SystemHub.plugin_name_mapping",
        "modulename": "open_precision.system_hub",
        "qualname": "SystemHub.plugin_name_mapping",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": dict[str, object]"
    }, {
        "fullname": "open_precision.system_hub.SystemHub.data",
        "modulename": "open_precision.system_hub",
        "qualname": "SystemHub.data",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": open_precision.managers.data_manager.DataManager"
    }, {
        "fullname": "open_precision.system_hub.SystemHub.system_task_manager",
        "modulename": "open_precision.system_hub",
        "qualname": "SystemHub.system_task_manager",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": open_precision.managers.system_task_manager.SystemTaskManager"
    }, {
        "fullname": "open_precision.system_hub.SystemHub.api",
        "modulename": "open_precision.system_hub",
        "qualname": "SystemHub.api",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": open_precision.api.API"
    }, {
        "fullname": "open_precision.system_hub.SystemHub.reload",
        "modulename": "open_precision.system_hub",
        "qualname": "SystemHub.reload",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.utils",
        "modulename": "open_precision.utils",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.utils.math",
        "modulename": "open_precision.utils.math",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.utils.math.get_rotation_matrix_ypr",
        "modulename": "open_precision.utils.math",
        "qualname": "get_rotation_matrix_ypr",
        "kind": "function",
        "doc": "<p>Rotationsmatrix f\u00fcr y=yaw, p=pitch, r=roll in degrees</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">y</span>, </span><span class=\"param\"><span class=\"n\">p</span>, </span><span class=\"param\"><span class=\"n\">r</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.utils.math.get_rotation_matrix_ypr_array",
        "modulename": "open_precision.utils.math",
        "qualname": "get_rotation_matrix_ypr_array",
        "kind": "function",
        "doc": "<p>Rotationsmatrix f\u00fcr y=yaw, p=pitch, r=roll in degrees</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">rotation_array</span><span class=\"p\">:</span> <span class=\"o\">&lt;</span><span class=\"n\">built</span><span class=\"o\">-</span><span class=\"ow\">in</span> <span class=\"n\">function</span> <span class=\"n\">array</span><span class=\"o\">&gt;</span></span><span class=\"return-annotation\">) -> <span class=\"o\">&lt;</span><span class=\"n\">built</span><span class=\"o\">-</span><span class=\"ow\">in</span> <span class=\"n\">function</span> <span class=\"n\">array</span><span class=\"o\">&gt;</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.utils.math.declination_from_vector",
        "modulename": "open_precision.utils.math",
        "qualname": "declination_from_vector",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">vector</span><span class=\"p\">:</span> <span class=\"o\">&lt;</span><span class=\"n\">built</span><span class=\"o\">-</span><span class=\"ow\">in</span> <span class=\"n\">function</span> <span class=\"n\">array</span><span class=\"o\">&gt;</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">float</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.utils.math.inclination_from_vector",
        "modulename": "open_precision.utils.math",
        "qualname": "inclination_from_vector",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">vector</span><span class=\"p\">:</span> <span class=\"o\">&lt;</span><span class=\"n\">built</span><span class=\"o\">-</span><span class=\"ow\">in</span> <span class=\"n\">function</span> <span class=\"n\">array</span><span class=\"o\">&gt;</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">float</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.utils.math.angle_between_vectors",
        "modulename": "open_precision.utils.math",
        "qualname": "angle_between_vectors",
        "kind": "function",
        "doc": "<p>returns angle between vector_a and vector_b as radian</p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">vector_a</span><span class=\"p\">:</span> <span class=\"o\">&lt;</span><span class=\"n\">built</span><span class=\"o\">-</span><span class=\"ow\">in</span> <span class=\"n\">function</span> <span class=\"n\">array</span><span class=\"o\">&gt;</span>,</span><span class=\"param\">\t<span class=\"n\">vector_b</span><span class=\"p\">:</span> <span class=\"o\">&lt;</span><span class=\"n\">built</span><span class=\"o\">-</span><span class=\"ow\">in</span> <span class=\"n\">function</span> <span class=\"n\">array</span><span class=\"o\">&gt;</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.utils.math.norm_vector",
        "modulename": "open_precision.utils.math",
        "qualname": "norm_vector",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">vec</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.utils.math.calc_distance",
        "modulename": "open_precision.utils.math",
        "qualname": "calc_distance",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">loc1</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">location</span><span class=\"o\">.</span><span class=\"n\">Location</span>,</span><span class=\"param\">\t<span class=\"n\">loc2</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">location</span><span class=\"o\">.</span><span class=\"n\">Location</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">float</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.utils.math.calc_distance_to_line",
        "modulename": "open_precision.utils.math",
        "qualname": "calc_distance_to_line",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">loc1</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">location</span><span class=\"o\">.</span><span class=\"n\">Location</span>,</span><span class=\"param\">\t<span class=\"n\">line_base_point</span><span class=\"p\">:</span> <span class=\"n\">open_precision</span><span class=\"o\">.</span><span class=\"n\">core</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">location</span><span class=\"o\">.</span><span class=\"n\">Location</span>,</span><span class=\"param\">\t<span class=\"n\">line_direction</span><span class=\"p\">:</span> <span class=\"o\">&lt;</span><span class=\"n\">built</span><span class=\"o\">-</span><span class=\"ow\">in</span> <span class=\"n\">function</span> <span class=\"n\">array</span><span class=\"o\">&gt;</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">float</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.utils.math.intersections_of_circle_and_line_segment",
        "modulename": "open_precision.utils.math",
        "qualname": "intersections_of_circle_and_line_segment",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">point_translated_1</span><span class=\"p\">:</span> <span class=\"nb\">tuple</span><span class=\"p\">[</span><span class=\"nb\">float</span><span class=\"p\">,</span> <span class=\"nb\">float</span><span class=\"p\">]</span>,</span><span class=\"param\">\t<span class=\"n\">point_translated_2</span><span class=\"p\">:</span> <span class=\"nb\">tuple</span><span class=\"p\">[</span><span class=\"nb\">float</span><span class=\"p\">,</span> <span class=\"nb\">float</span><span class=\"p\">]</span>,</span><span class=\"param\">\t<span class=\"n\">circle_radius</span><span class=\"p\">:</span> <span class=\"nb\">float</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">tuple</span><span class=\"p\">[</span><span class=\"nb\">float</span><span class=\"p\">,</span> <span class=\"nb\">float</span><span class=\"p\">]]</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.utils.neomodel",
        "modulename": "open_precision.utils.neomodel",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.utils.neomodel.DillProperty",
        "modulename": "open_precision.utils.neomodel",
        "qualname": "DillProperty",
        "kind": "class",
        "doc": "<p>Property for storing data in a Neo4j database using dill serialization.</p>\n",
        "bases": "neomodel.properties.Property, typing.Generic[~T]"
    }, {
        "fullname": "open_precision.utils.neomodel.DillProperty.inflate",
        "modulename": "open_precision.utils.neomodel",
        "qualname": "DillProperty.inflate",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">value</span><span class=\"p\">:</span> <span class=\"nb\">str</span></span><span class=\"return-annotation\">) -> <span class=\"o\">~</span><span class=\"n\">T</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.utils.neomodel.DillProperty.deflate",
        "modulename": "open_precision.utils.neomodel",
        "qualname": "DillProperty.deflate",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">value</span><span class=\"p\">:</span> <span class=\"o\">~</span><span class=\"n\">T</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">str</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.utils.other",
        "modulename": "open_precision.utils.other",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.utils.other.async_partial",
        "modulename": "open_precision.utils.other",
        "qualname": "async_partial",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">f</span>, </span><span class=\"param\"><span class=\"o\">*</span><span class=\"n\">args</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.utils.other.is_iterable",
        "modulename": "open_precision.utils.other",
        "qualname": "is_iterable",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">obj</span><span class=\"p\">:</span> <span class=\"o\">&lt;</span><span class=\"n\">built</span><span class=\"o\">-</span><span class=\"ow\">in</span> <span class=\"n\">function</span> <span class=\"nb\">any</span><span class=\"o\">&gt;</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.utils.other.get_attributes",
        "modulename": "open_precision.utils.other",
        "qualname": "get_attributes",
        "kind": "function",
        "doc": "<p>Get all attributes of a class and its base classes recursively.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>cls</strong>: </li>\n<li><strong>base_filter</strong>:  func to filter base classes, inherited paths will be ignored above classes that do not pass the filter</li>\n<li><strong>property_name_filter</strong>:  func to filter property names, properties will be ignored if filter returns False</li>\n<li><strong>property_type_filter</strong>:  func to filter property types, properties will be ignored if filter returns False</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>a set of all property names of the class (including inherited ones)</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">cls</span>,</span><span class=\"param\">\t<span class=\"n\">base_filter</span><span class=\"p\">:</span> <span class=\"n\">Callable</span><span class=\"p\">[[</span><span class=\"nb\">type</span><span class=\"p\">],</span> <span class=\"nb\">bool</span><span class=\"p\">]</span> <span class=\"o\">=</span> <span class=\"o\">&lt;</span><span class=\"n\">function</span> <span class=\"o\">&lt;</span><span class=\"k\">lambda</span><span class=\"o\">&gt;&gt;</span>,</span><span class=\"param\">\t<span class=\"n\">property_name_filter</span><span class=\"p\">:</span> <span class=\"n\">Callable</span><span class=\"p\">[[</span><span class=\"nb\">str</span><span class=\"p\">],</span> <span class=\"nb\">bool</span><span class=\"p\">]</span> <span class=\"o\">=</span> <span class=\"o\">&lt;</span><span class=\"n\">function</span> <span class=\"o\">&lt;</span><span class=\"k\">lambda</span><span class=\"o\">&gt;&gt;</span>,</span><span class=\"param\">\t<span class=\"n\">property_type_filter</span><span class=\"p\">:</span> <span class=\"n\">Callable</span><span class=\"p\">[[</span><span class=\"nb\">type</span><span class=\"p\">],</span> <span class=\"nb\">bool</span><span class=\"p\">]</span> <span class=\"o\">=</span> <span class=\"o\">&lt;</span><span class=\"n\">function</span> <span class=\"o\">&lt;</span><span class=\"k\">lambda</span><span class=\"o\">&gt;&gt;</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">frozenset</span><span class=\"p\">[</span><span class=\"nb\">str</span><span class=\"p\">]</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.utils.other.millis",
        "modulename": "open_precision.utils.other",
        "qualname": "millis",
        "kind": "function",
        "doc": "<p></p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "open_precision.utils.validation",
        "modulename": "open_precision.utils.validation",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "open_precision.utils.validation.validate_value",
        "modulename": "open_precision.utils.validation",
        "qualname": "validate_value",
        "kind": "function",
        "doc": "<p>Checks if value is valid according to rule.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>value</strong>:  value to check</li>\n<li><strong>rule</strong>:  func that returns True if value is valid</li>\n<li><strong>rule_description</strong>:  description of rule for error message</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>True if value is valid according to rule, raises ValueError otherwise</p>\n</blockquote>\n\n<h6 id=\"raises\">Raises</h6>\n\n<ul>\n<li><strong>ValueError</strong>:  if value is not valid according to rule</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">value</span><span class=\"p\">:</span> <span class=\"n\">Any</span>,</span><span class=\"param\">\t<span class=\"n\">rule</span><span class=\"p\">:</span> <span class=\"n\">Callable</span><span class=\"p\">[[</span><span class=\"n\">Any</span><span class=\"p\">],</span> <span class=\"nb\">bool</span><span class=\"p\">]</span>,</span><span class=\"param\">\t<span class=\"n\">rule_description</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">bool</span>:</span></span>",
        "funcdef": "def"
    }];

    // mirrored in build-search-index.js (part 1)
    // Also split on html tags. this is a cheap heuristic, but good enough.
    elasticlunr.tokenizer.setSeperator(/[\s\-.;&_'"=,()]+|<[^>]*>/);

    let searchIndex;
    if (docs._isPrebuiltIndex) {
        console.info("using precompiled search index");
        searchIndex = elasticlunr.Index.load(docs);
    } else {
        console.time("building search index");
        // mirrored in build-search-index.js (part 2)
        searchIndex = elasticlunr(function () {
            this.pipeline.remove(elasticlunr.stemmer);
            this.pipeline.remove(elasticlunr.stopWordFilter);
            this.addField("qualname");
            this.addField("fullname");
            this.addField("annotation");
            this.addField("default_value");
            this.addField("signature");
            this.addField("bases");
            this.addField("doc");
            this.setRef("fullname");
        });
        for (let doc of docs) {
            searchIndex.addDoc(doc);
        }
        console.timeEnd("building search index");
    }

    return (term) => searchIndex.search(term, {
        fields: {
            qualname: {boost: 4},
            fullname: {boost: 2},
            annotation: {boost: 2},
            default_value: {boost: 2},
            signature: {boost: 2},
            bases: {boost: 2},
            doc: {boost: 1},
        },
        expand: true
    });
})();