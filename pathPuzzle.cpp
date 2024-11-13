#include <iostream>
#include <functional>
#include <vector>
#include <numeric>

using namespace std;

class Solution {
    int dx[4] = { 0, 0, 1, -1 };
    int dy[4] = { 1, -1, 0, 0 };
public:
    vector<int> pathPuzzle(int col[], int row[], int n) {
        vector<vector<bool>> vis(n, vector<bool>(n, false));
        vector<int> path;
        function<bool(int, int)> dfs = [&](int x, int y) {
            if (x < 0 || x >= n || y < 0 || y >= n) return false;
            if (vis[x][y]) return false;
            if (row[x] == 0 || col[y] == 0) return false;

            row[x]--;
            col[y]--;
            vis[x][y] = true;
            path.push_back(x * n + y);

            if (x == n - 1 && y == n - 1 &&
                accumulate(row, row + n, 0) == 0 &&
                accumulate(col, col + n, 0) == 0) return true;

            for (int d = 0; d < 4; d++) {
                if (dfs(x + dx[d], y + dy[d])) return true;
            }

            row[x]++;
            col[y]++;
            vis[x][y] = false;
            path.pop_back();
            return false;
        };
        dfs(0, 0);
        return path;
    };
};

int main()
{
    int n;
    cin >> n;
    int* row = new int[n], * col = new int[n];
    Solution s;
    for (int i = 0; i < n; i++) cin >> col[i];
    for (int i = 0; i < n; i++) cin >> row[i];
    vector<int> path = s.pathPuzzle(col, row, n);
    for (auto p : path) cout << p << ' ';
    cout << endl;
    delete [] row;
    delete [] col;
    return 0;
}
