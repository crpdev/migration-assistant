import * as vscode from 'vscode';

export class MigrationStep extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly status: 'pending' | 'in_progress' | 'completed' | 'error',
        public readonly details?: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState = vscode.TreeItemCollapsibleState.None
    ) {
        super(label, collapsibleState);
        this.tooltip = details || label;
        this.description = this.getStatusIcon();
    }

    private getStatusIcon(): string {
        switch (this.status) {
            case 'pending':
                return '⏳';
            case 'in_progress':
                return '🔄';
            case 'completed':
                return '✅';
            case 'error':
                return '❌';
            default:
                return '';
        }
    }
}

export class MigrationStepsProvider implements vscode.TreeDataProvider<MigrationStep> {
    private _onDidChangeTreeData: vscode.EventEmitter<MigrationStep | undefined | null | void> = new vscode.EventEmitter<MigrationStep | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<MigrationStep | undefined | null | void> = this._onDidChangeTreeData.event;

    private steps: MigrationStep[] = [];

    constructor() {
        this.initializeSteps();
    }

    private initializeSteps() {
        this.steps = [
            new MigrationStep('Project Exploration', 'pending'),
            new MigrationStep('POM Analysis', 'pending'),
            new MigrationStep('Spring Boot Verification', 'pending'),
            new MigrationStep('Initial Compilation', 'pending'),
            new MigrationStep('Test Execution', 'pending'),
            new MigrationStep('Migration Path Determination', 'pending'),
            new MigrationStep('Migration Execution', 'pending'),
            new MigrationStep('Post-migration Verification', 'pending'),
            new MigrationStep('Report Generation', 'pending')
        ];
    }

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    updateStep(index: number, status: 'pending' | 'in_progress' | 'completed' | 'error', details?: string) {
        if (index >= 0 && index < this.steps.length) {
            this.steps[index] = new MigrationStep(
                this.steps[index].label,
                status,
                details
            );
            this.refresh();
        }
    }

    getTreeItem(element: MigrationStep): vscode.TreeItem {
        return element;
    }

    getChildren(element?: MigrationStep): Thenable<MigrationStep[]> {
        if (!element) {
            return Promise.resolve(this.steps);
        }
        return Promise.resolve([]);
    }
} 