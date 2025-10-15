"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.PatternsProvider = void 0;
const vscode = __importStar(require("vscode"));
class PatternsProvider {
    constructor(ultrathinkService) {
        this.ultrathinkService = ultrathinkService;
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
    }
    refresh() {
        this._onDidChangeTreeData.fire();
    }
    getTreeItem(element) {
        return element;
    }
    getChildren(element) {
        if (element) {
            return Promise.resolve([]);
        }
        const patterns = this.ultrathinkService.getPatterns();
        if (patterns.length === 0) {
            return Promise.resolve([
                new PatternItem('No patterns learned yet', 'Run "Learn Patterns" to start', 0, 'unknown')
            ]);
        }
        const sorted = patterns.sort((a, b) => b.frequency - a.frequency);
        return Promise.resolve(sorted.map(p => new PatternItem(p.description, `${p.category} • ${p.frequency}x`, p.frequency, p.category)));
    }
}
exports.PatternsProvider = PatternsProvider;
class PatternItem extends vscode.TreeItem {
    constructor(label, description, frequency, category) {
        super(label, vscode.TreeItemCollapsibleState.None);
        this.label = label;
        this.description = description;
        this.frequency = frequency;
        this.category = category;
        this.tooltip = `${label}\n${description}`;
        this.description = description;
        this.iconPath = this.getIcon(category);
    }
    getIcon(category) {
        const iconMap = {
            bug: 'bug',
            security: 'shield',
            quality: 'star',
            performance: 'zap',
            style: 'paintcan'
        };
        return new vscode.ThemeIcon(iconMap[category] || 'lightbulb');
    }
}
//# sourceMappingURL=patternsProvider.js.map